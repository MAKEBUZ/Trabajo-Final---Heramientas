from pathlib import Path
import csv
try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None


def leer_estadisticas(csv_path: Path):
    """
    Lee: target,ids,date,flag,user,text (latin-1)
    Calcula por grupo (0,2,4): n, suma longitudes y suma de cuadrados.
    """
    grupos = {0: {"n": 0, "sum": 0.0, "sumsq": 0.0},
              2: {"n": 0, "sum": 0.0, "sumsq": 0.0},
              4: {"n": 0, "sum": 0.0, "sumsq": 0.0}}
    with csv_path.open(newline="", encoding="latin-1") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                t = int(row.get("target", ""))
            except Exception:
                continue
            if t not in grupos:
                continue
            L = len(row.get("text", ""))
            g = grupos[t]
            g["n"] += 1
            g["sum"] += L
            g["sumsq"] += L * L

    # Convertir a mean/var
    stats = {}
    for t, g in grupos.items():
        n = g["n"]
        if n > 0:
            mean = g["sum"] / n
            var = (g["sumsq"] - (g["sum"] ** 2) / n) / (n - 1) if n > 1 else 0.0
        else:
            mean = 0.0
            var = 0.0
        stats[t] = {"n": n, "mean": mean, "var": var}
    return stats


def leer_longitudes(csv_path: Path):
    grupos = {0: [], 2: [], 4: []}
    with csv_path.open(newline="", encoding="latin-1") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                t = int(row.get("target", ""))
            except Exception:
                continue
            if t not in grupos:
                continue
            L = len(row.get("text", ""))
            grupos[t].append(L)
    return grupos


def anova(stats):
    """ANOVA de un factor desde estadísticas agregadas."""
    present = [s for s in stats.values() if s["n"] > 0]
    k = len(present)
    N = sum(s["n"] for s in present)
    if k < 2 or N <= k:
        return None

    grand_mean = sum(s["mean"] * s["n"] for s in present) / N
    SSB = sum(s["n"] * (s["mean"] - grand_mean) ** 2 for s in present)
    SSE = sum((s["n"] - 1) * s["var"] for s in present)
    df1, df2 = k - 1, N - k
    if SSE <= 0:
        return None
    MSB, MSE = SSB / df1, SSE / df2
    F = MSB / MSE

    # p-value opcional (SciPy)
    p = None
    try:
        from scipy.stats import f as f_dist  # type: ignore
        p = float(f_dist.sf(F, df1, df2))
    except Exception:
        pass
    return {"F": F, "df1": df1, "df2": df2, "p": p, "grand_mean": grand_mean}


def pruebas_normalidad(lengths):
    res = {0: {"shapiro": None, "dagostino": None}, 2: {"shapiro": None, "dagostino": None}, 4: {"shapiro": None, "dagostino": None}}
    try:
        from scipy.stats import shapiro, normaltest
        for t in (0, 2, 4):
            xs = lengths.get(t, [])
            if len(xs) >= 3:
                try:
                    w, p = shapiro(xs[:5000])
                    res[t]["shapiro"] = {"stat": float(w), "p": float(p)}
                except Exception:
                    res[t]["shapiro"] = None
            if len(xs) >= 8:
                try:
                    k2, p2 = normaltest(xs)
                    res[t]["dagostino"] = {"stat": float(k2), "p": float(p2)}
                except Exception:
                    res[t]["dagostino"] = None
    except Exception:
        pass
    return res


def homogeneidad_test(lengths):
    try:
        from scipy.stats import levene
        grupos = [g for g in (lengths.get(0, []), lengths.get(2, []), lengths.get(4, [])) if len(g) > 1]
        if len(grupos) >= 2:
            stat, p = levene(*grupos)
            return {"stat": float(stat), "p": float(p)}
    except Exception:
        return None
    return None


def kruskal_wallis(lengths):
    try:
        from scipy.stats import kruskal
        grupos = [g for g in (lengths.get(0, []), lengths.get(2, []), lengths.get(4, [])) if len(g) > 0]
        if len(grupos) >= 2:
            h, p = kruskal(*grupos)
            return {"H": float(h), "p": float(p)}
    except Exception:
        return None
    return None


def grafico_histogramas(lengths, base: Path):
    if plt is None:
        return []
    label = {0: "negativo", 2: "neutral", 4: "positivo"}
    rutas = []
    for t in (0, 2, 4):
        xs = lengths.get(t, [])
        if not xs:
            continue
        fig = plt.figure(figsize=(6, 4))
        plt.hist(xs, bins=30, color="#4C78A8", alpha=0.9)
        plt.title(f"Histograma longitud – {label.get(t)}")
        plt.xlabel("longitud")
        plt.ylabel("frecuencia")
        ruta = base / f"AnovaTweets2_hist_{t}.png"
        fig.tight_layout()
        fig.savefig(ruta)
        plt.close(fig)
        rutas.append(str(ruta))
    return rutas


def grafico_boxplot(lengths, base: Path):
    if plt is None:
        return None
    datos = []
    etiquetas = []
    label = {0: "negativo", 2: "neutral", 4: "positivo"}
    for t in (0, 2, 4):
        xs = lengths.get(t, [])
        if xs:
            datos.append(xs)
            etiquetas.append(label.get(t))
    if not datos:
        return None
    fig = plt.figure(figsize=(7, 5))
    plt.boxplot(datos, labels=etiquetas, showmeans=True)
    plt.title("Boxplot longitud por sentimiento")
    plt.ylabel("longitud")
    ruta = base / "AnovaTweets2_boxplot.png"
    fig.tight_layout()
    fig.savefig(ruta)
    plt.close(fig)
    return str(ruta)


def grafico_qq(lengths, base: Path):
    if plt is None:
        return []
    rutas = []
    try:
        from scipy.stats import probplot
    except Exception:
        return []
    label = {0: "negativo", 2: "neutral", 4: "positivo"}
    for t in (0, 2, 4):
        xs = lengths.get(t, [])
        if len(xs) >= 3:
            fig = plt.figure(figsize=(6, 4))
            probplot(xs, dist="norm", plot=plt)
            plt.title(f"QQ plot normal – {label.get(t)}")
            ruta = base / f"AnovaTweets2_qq_{t}.png"
            fig.tight_layout()
            fig.savefig(ruta)
            plt.close(fig)
            rutas.append(str(ruta))
    return rutas


def grafico_varianzas(stats, base: Path):
    if plt is None:
        return None
    etiquetas = []
    valores = []
    label = {0: "negativo", 2: "neutral", 4: "positivo"}
    for t in (0, 2, 4):
        s = stats.get(t)
        etiquetas.append(label.get(t))
        valores.append(s["var"])
    fig = plt.figure(figsize=(7, 5))
    plt.bar(etiquetas, valores, color="#F58518")
    plt.title("Varianzas por grupo")
    plt.ylabel("varianza")
    ruta = base / "AnovaTweets2_varianzas.png"
    fig.tight_layout()
    fig.savefig(ruta)
    plt.close(fig)
    return str(ruta)


def reporte(stats, res, normal=None, kw=None, hom=None, figuras=None):
    label = {0: "negativo", 2: "neutral", 4: "positivo"}
    L = []
    L.append("Prueba ANOVA (básica) – Longitud promedio del tweet por sentimiento")
    L.append("")
    L.append("Objetivo: Comparar la longitud promedio del tweet entre categorías de sentimiento.")
    L.append("Hipótesis:")
    L.append("  H₀: Las medias son iguales.")
    L.append("  H₁: Al menos una difiere.")
    L.append("Supuestos: normalidad y homogeneidad; si no se cumplen, usar Kruskal–Wallis.")
    L.append("")

    L.append("Estadísticos por grupo (longitud de texto):")
    for t in (0, 2, 4):
        s = stats.get(t)
        L.append(
            f"  target = {t} ({label.get(t)}): n = {s['n']}, media = {s['mean']:.6f}, var = {s['var']:.6f}"
        )

    zeros = [label[t] for t, s in stats.items() if s["n"] == 0]
    if zeros:
        L.append("")
        L.append("Nota: Categorías sin datos (n = 0) excluidas en inferencia: " + ", ".join(zeros))

    L.append("")
    if res is None:
        L.append("ANOVA no ejecutado: requieren ≥2 grupos con n>0 y SSE>0.")
        return "\n".join(L)

    L.append(f"Media global: {res['grand_mean']:.6f}")
    L.append(f"ANOVA: F({res['df1']}, {res['df2']}) = {res['F']:.6f}")
    if res["p"] is not None:
        L.append(f"p-value (SciPy): {res['p']:.50f} (~{res['p']:.6g})")
    else:
        L.append("p-value: no calculado (SciPy no disponible)")

    # Diferencia descriptiva entre negativo y positivo si existen
    if stats[0]["n"] > 0 and stats[4]["n"] > 0:
        diff = stats[0]["mean"] - stats[4]["mean"]
        pct = (diff / stats[4]["mean"]) * 100 if stats[4]["mean"] else 0.0
        L.append("")
        L.append("Comparación descriptiva de medias:")
        L.append(f"  negativo vs positivo: Δ media = {diff:.6f} caracteres ({pct:.3f}%)")

    L.append("")
    L.append("Interpretación:")
    L.append("- Si p << 0.05, se rechaza H₀ y se concluye H₁ (al menos una difiere).")
    L.append("- La diferencia observada debe evaluarse por su relevancia práctica además de la significancia.")
    L.append("")
    L.append("Pruebas adicionales y gráficos:")
    if normal is not None:
        for t in (0, 2, 4):
            s = normal.get(t, {})
            if s.get("shapiro") is not None:
                L.append(f"  Normalidad Shapiro {label.get(t)}: W = {s['shapiro']['stat']:.6f}, p = {s['shapiro']['p']:.6g}")
            if s.get("dagostino") is not None:
                L.append(f"  Normalidad D'Agostino {label.get(t)}: K2 = {s['dagostino']['stat']:.6f}, p = {s['dagostino']['p']:.6g}")
    if hom is not None:
        L.append(f"  Homogeneidad (Levene): estadístico = {hom['stat']:.6f}, p = {hom['p']:.6g}")
    if kw is not None:
        L.append(f"  Kruskal–Wallis: H = {kw['H']:.6f}, p = {kw['p']:.6g}")
    if figuras:
        L.append("  Figuras guardadas:")
        for r in figuras:
            L.append(f"    {r}")
    return "\n".join(L)


def main():
    base = Path(__file__).resolve().parent
    csv_path = base / "part-00000-d12a28b9-ec6a-47ca-b0a6-fa90cb633f14-c000.csv"
    if not csv_path.exists():
        print(f"No se encuentra el archivo: {csv_path}")
        return
    stats = leer_estadisticas(csv_path)
    res = anova(stats)
    lengths = leer_longitudes(csv_path)
    normal = pruebas_normalidad(lengths)
    hom = homogeneidad_test(lengths)
    kw = kruskal_wallis(lengths)
    figuras = []
    figuras += grafico_histogramas(lengths, base)
    bp = grafico_boxplot(lengths, base)
    if bp:
        figuras.append(bp)
    figuras += grafico_qq(lengths, base)
    varb = grafico_varianzas(stats, base)
    if varb:
        figuras.append(varb)
    text = reporte(stats, res, normal=normal, kw=kw, hom=hom, figuras=figuras)
    out = base / "AnovaTweets2_report.txt"
    out.write_text(text, encoding="utf-8")
    print(text)
    print("")
    print(f"Informe guardado en: {out}")


if __name__ == "__main__":
    main()