from playwright.async_api import async_playwright
ARBITR_URL = "https://kad.arbitr.ru"


def _print_log(i: str, t: str = None):
    prefix = "ERROR" if t == 'e' else "INFO"
    print(f"{prefix} | Cookie Update | {i}")


async def get_cookies_dict(headless: bool = True, debug: bool = False):
    data = await get_browser_data(headless, debug)
    return {cookie['name']: cookie['value'] for cookie in data['cookies']}


async def get_browser_data(headless: bool = True, debug: bool = False):
    result = {'success': False, 'cookies': [], 'error': None}
    
    async with async_playwright() as p:
        browser = None
        context = None
        page = None
        
        try:
            # Инициализация браузера
            browser = await p.chromium.launch(
                headless=headless,
                args=[
                    '--enable-features=WebAssembly',
                    '--enable-webgl',
                    '--enable-accelerated-2d-canvas',
                    '--font-render-hinting=none',
                    '--disable-gpu',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process',
                    '--disable-site-isolation-trials',
                    '--use-gl=desktop',
                    '--mute-audio',
                    '--no-first-run',
                    '--no-sandbox',
                    '--hide-scrollbars',
                    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    '--window-size=1280,720'
                ],
                chromium_sandbox=False,
                firefox_user_prefs={
                    "privacy.resistFingerprinting": False,
                    "dom.webdriver.enabled": False
                }
            )
            
            # Создание контекста
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1280, 'height': 720},
                locale='ru-RU',
                timezone_id='Europe/Moscow',
                bypass_csp=True,
                java_script_enabled=True,
                ignore_https_errors=True,
                extra_http_headers={
                'Accept': '*/*',
                'Wasm-Support': 'true'
                }
            )
            
            blocked_domains = [
                "mail.ru",
                "yandex",
                "vk.com",
                "google-analytics",
                "googletagmanager",
                "doubleclick.net",
            ]

            async def blocker(route):
                url = route.request.url
                if any(dom in url for dom in blocked_domains):
                    await route.abort()
                else:
                    await route.continue_()

            await context.route("**/*", blocker)

            await context.add_init_script(
                """
                (() => {
                const NativeWS = window.WebSocket;
                function FakeWS(url, protocols) {
                    // Блокируем только "itsgonnafail", остальные WS работают как обычно
                    if (url.includes('itsgonnafail')) {
                    console.info('[stealth] WebSocket to', url, 'blocked');
                    // minimal stub — сразу закрытое соединение
                    this.readyState = 3; 
                    this.CONNECTING = 0;
                    this.OPEN       = 1;
                    this.CLOSING    = 2;
                    this.CLOSED     = 3;
                    // вешаем no-op обработчики
                    this.send = () => {};
                    this.close = () => {};
                    return;
                    }   
                    // для остальных создаём «настоящий» WS
                    return new NativeWS(url, protocols);
                }
                // Наследуем прототип, сохраняя все методы
                FakeWS.prototype = NativeWS.prototype;
                window.WebSocket = FakeWS;
                })();
                """
            )

           # Создание страницы
            page = await context.new_page()

            if debug:
                def log_request(request):
                    _print_log(f"Request: {request.method} {request.url}")

                def log_response(response):
                    if response.status >= 400:
                        _print_log(f"Response Error: {response.status} {response.url}", 'e')

                def log_console(msg):
                    if msg.type == 'error':
                        _print_log(f"Console Error: {msg.text}", 'e')

                def log_page_error(error):
                    _print_log(f"Page Error: {error}", 'e')

                await page.expose_function('wasmLog', lambda msg: _print_log(f"WASM: {msg}"))
                await page.evaluate('''() => {
                    WebAssembly.instantiateStreaming = async (response, importObject) => {
                        const bytes = await response.arrayBuffer();
                        window.wasmLog(`Loaded ${bytes.byteLength} bytes`);
                        return WebAssembly.instantiate(bytes, importObject);
                    };
                }''')

                page.on("request", log_request)
                page.on("response", log_response)
                page.on("console", log_console)
                page.on("pageerror", log_page_error)

            _print_log('Client initialized')

            # Навигация с улучшенным ожиданием
            await page.goto(
                ARBITR_URL,
                wait_until='networkidle',
                timeout=10000
            )
            _print_log('Main page loaded')

            # Закрытие промо-окна
            try:
                close_button = await page.wait_for_selector(
                    '.js-promo_notification-popup-close',
                    state='visible',
                    timeout=3000
                )
                await close_button.click()
                await page.wait_for_selector(
                    '.js-promo_notification-popup-close', 
                    state='hidden', 
                    timeout=3000)
                _print_log('Promo window closed')
            except Exception as e:
                _print_log(f"Promo error: {str(e)}", 'e')
            finally:
                await page.wait_for_timeout(100)

            await page.evaluate('''() => {
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => false
                });
            }''')

            if headless:
                await page.mouse.move(100, 100, steps=10)

            await page.evaluate('''async () => {
                await new Promise(requestAnimationFrame);
                await new Promise(resolve => setTimeout(resolve, 250));
            }''')

            # Нажатие основной кнопки
            try:
                submit_button = await page.wait_for_selector(
                    '#b-form-submit button',
                    timeout=3000
                )
                await submit_button.click(delay=100)
                _print_log('Submit button clicked and navigation completed')
            except Exception as e:
                _print_log(f"Click error: {str(e)}", 'e')
            finally:
                pass

            # Ожидание куки
            await page.wait_for_function(
                '''async () => {
                const hasCookies = () => 
                    document.cookie.includes('pr_fp') && 
                    document.cookie.includes('wasm');
                
                let delay = 500; // Стартовая задержка
                for(let i = 0; i < 15; i++) { // Уменьшаем кол-во попыток
                    if(hasCookies()) return true;
                    console.log('Waiting for cookies... attempt:', i + 1);
                    await new Promise(r => setTimeout(r, delay));
                    delay *= 1.5; // Экспоненциальное увеличение задержки
                }
                return false;
                }''',
                timeout=10000
            )

            await page.wait_for_timeout(1000)
            _print_log('Collect cookies')

            # Сбор куки
            cookies = await context.cookies('https://kad.arbitr.ru')
            result['cookies'] = [{
                'name': c['name'],
                'value': c['value'],
                'domain': c['domain'],
                'path': c['path'],
                'expires': c['expires']
            } for c in cookies]

            result['success'] = True

        except Exception as e:
            result['error'] = str(e)
            _print_log(str(e), 'e')
            
            if debug and page and not page.is_closed():
                try:
                    await page.screenshot(path='debug_screenshot.png')
                    _print_log('Debug screenshot saved')
                except Exception as screenshot_error:
                    _print_log(f"Screenshot error: {str(screenshot_error)}", 'e')

        finally:
            try:
                if page and not page.is_closed():
                    await page.close()
                if context:
                    await context.close()
                if browser:
                    await browser.close()
            except Exception as close_error:
                _print_log(f"Cleanup error: {str(close_error)}", 'e')

    return result


if __name__ == "__main__":
    import argparse
    import asyncio

    def parse_args():
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            '-h', '--headless', 
            action='store_true',
            help='Запуск в headless-режиме (без графического интерфейса)'
        )
        parser.add_argument(
            '-d', '--debug', 
            action='store_true',
            help='Включить режим отладки (логирование и скриншоты)'
        )
        parser.add_argument(
            '--help', 
            action='help', 
            default=argparse.SUPPRESS,
            help='Показать это сообщение и выйти'
        )
        return parser.parse_args()

    args = parse_args()
    cookies = asyncio.run(get_cookies_dict(
        headless=args.headless,
        debug=args.debug
    ))
    print(cookies)
