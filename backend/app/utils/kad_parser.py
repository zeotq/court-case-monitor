from bs4 import BeautifulSoup
import re

class SearchResponseParser:
    @staticmethod
    def clean_text(text):
        """Очищает строку от лишних пробелов, переносов и табуляций."""
        if not text:
            return None
        return re.sub(r'\s+', ' ', text).strip()

    @staticmethod
    def parse(html):
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.find_all("tr")

        cases = []
        for row in rows:
            case_data = {}

            # Дата и номер дела
            num_td = row.find("td", class_="num")
            if num_td:
                date_div = num_td.find("div", {"title": True})
                if date_div:
                    case_data["date"] = SearchResponseParser.clean_text(date_div.get("title", ""))
                    type_class = date_div.get("class", [])
                    case_data["case_type"] = type_class[0] if type_class and len(type_class) > 0 else 'default'

                case_link = num_td.find("a", class_="num_case")
                if case_link:
                    case_data["case_number"] = SearchResponseParser.clean_text(case_link.text)
                    href = case_link.get("href", "")
                    if not href.startswith("http"):
                        href = "https://kad.arbitr.ru" + href
                    case_data["case_link"] = href

            # Суд и судья
            court_td = row.find("td", class_="court")
            if court_td:
                court_div = court_td.find("div", {"title": True}, class_=lambda x: x != "judge")
                if court_div:
                    case_data["court"] = SearchResponseParser.clean_text(court_div.get("title", ""))

                judge_div = court_td.find("div", class_="judge")
                if judge_div:
                    case_data["judge"] = SearchResponseParser.clean_text(judge_div.get("title", ""))

            # Истец (plaintiff)
            plaintiff_td = row.find("td", class_="plaintiff")
            if plaintiff_td:
                plaintiff_span = plaintiff_td.find("span", class_="js-rollover")
                if plaintiff_span:
                    raw_name = plaintiff_span.find(text=True, recursive=False)
                    plaintiff_name = SearchResponseParser.clean_text(raw_name)
                else:
                    plaintiff_name = None

                # Извлекаем ИНН с помощью regex
                inn_value = None
                inn_div = plaintiff_td.find("div")
                if inn_div:
                    inn_search = re.search(r"ИНН:\s*(\d+)", inn_div.get_text())
                    if inn_search:
                        inn_value = inn_search.group(1)

                case_data["plaintiff"] = {
                    "name": plaintiff_name,
                    "inn": inn_value
                }

            # Ответчик (respondent)
            respondent_td = row.find("td", class_="respondent")
            if respondent_td:
                respondent_span = respondent_td.find("span", class_="js-rollover")
                if respondent_span:
                    raw_name = respondent_span.find(text=True, recursive=False)
                    respondent_name = SearchResponseParser.clean_text(raw_name)
                else:
                    respondent_name = None

                inn_value = None
                inn_div = respondent_td.find("div")
                if inn_div:
                    inn_search = re.search(r"ИНН:\s*(\d+)", inn_div.get_text())
                    if inn_search:
                        inn_value = inn_search.group(1)

                case_data["respondent"] = {
                    "name": respondent_name,
                    "inn": inn_value
                }

            if case_data:
                cases.append(case_data)

        # Информация о страницах с защитой от ошибок
        pagination_info = {}
        for key in ["documentsPageSize", "documentsPage", "documentsTotalCount", "documentsPagesCount"]:
            input_tag = soup.find("input", {"id": key})
            if input_tag:
                try:
                    pagination_info[key] = int(input_tag.get("value", "0"))
                except ValueError:
                    pagination_info[key] = input_tag.get("value")
            else:
                pagination_info[key] = None

        return {"cases": cases, "pagination": pagination_info}
    

def case_type_to_label(case_type):
    """Преобразует тип дела в человекочитаемую метку."""
    case_type_labels = {
        "default": "Общее дело",
        "civil": "Гражданское дело",
        "administrative": "Административное дело",
        "arbitration": "Арбитражное дело",
        "bankruptcy": "Банкртное дело",
    }
    return case_type_labels.get(case_type, "Неизвестный тип дела")


def case_type_to_litter(case_type):
    """Преобразует тип дела в первую букву."""
    case_type_litters = {
        "default": "N",
        "civil": "G",
        "administrative": "А",
        "arbitration": "S",
        "bankruptcy": "B",
    }
    return case_type_litters.get(case_type, "N")
