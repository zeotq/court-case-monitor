export default function Loading() {
  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center" }}>
      <div style={{
        fontSize: "48px",
        animation: "spin 2s linear infinite",
        display: "inline-block"
      }}>
        ♂
      </div>
      <style>
        {`
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
        `}
      </style>
    </div>
  );
}
