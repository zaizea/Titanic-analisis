import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "train.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "resultados"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

print("=" * 60)
print("ANÁLISIS EXPLORATORIO DEL TITANIC")
print("=" * 60)
print()

print("1. NÚMERO DE PASAJEROS")
print(f"Total de pasajeros: {len(df)}")
print()

print("2. NÚMERO DE COLUMNAS")
print(f"Total de columnas: {len(df.columns)}")
print()

print("3. VARIABLES DISPONIBLES")
print(df.columns.tolist())
print()

print("4. TIPOS DE DATOS")
print(df.dtypes)
print()

print("5. VALORES FALTANTES")
print(df.isnull().sum())
print()

print("6. REGISTROS DUPLICADOS")
print(df.duplicated().sum())
print()

print("7. ESTADÍSTICAS DESCRIPTIVAS")
print(df.describe())
print()

print("=" * 60)
print("LIMPIEZA Y PREPROCESAMIENTO")
print("=" * 60)
print()

df = df.drop_duplicates()

df["Age"] = df.groupby(
    ["Pclass", "Sex"]
)["Age"].transform(
    lambda x: x.fillna(x.median())
)

df["Age"] = df["Age"].fillna(df["Age"].median())

df["Embarked"] = df["Embarked"].fillna(
    df["Embarked"].mode()[0]
)

df["Cabin"] = df["Cabin"].fillna("Unknown")

df["FamilySize"] = df["SibSp"] + df["Parch"] + 1

df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

print("Limpieza de datos completada")

def clasificar_edad(edad):
    if edad < 13:
        return "Niño"
    elif edad < 20:
        return "Joven"
    elif edad < 60:
        return "Adulto"
    else:
        return "Adulto mayor"

df["AgeGroup"] = df["Age"].apply(clasificar_edad)

print("Valores faltantes después de la limpieza:")
print(df.isnull().sum())
print()

print("Nuevas variables creadas:")
print("FamilySize")
print("IsAlone")
print("AgeGroup")
print()

print("=" * 60)
print("ANÁLISIS 1: PORCENTAJE DE SUPERVIVENCIA")
print("=" * 60)
print()

survival_percentage = df["Survived"].mean() * 100

print(
    f"Porcentaje de pasajeros que sobrevivió: "
    f"{survival_percentage:.2f}%"
)

print(
    f"Porcentaje de pasajeros que no sobrevivió: "
    f"{100 - survival_percentage:.2f}%"
)
print()

print("=" * 60)
print("ANÁLISIS 2: SUPERVIVENCIA SEGÚN SEXO")
print("=" * 60)
print()

survival_sex = (
    df.groupby("Sex")["Survived"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

print(survival_sex)
print()

print("=" * 60)
print("ANÁLISIS 3: SUPERVIVENCIA SEGÚN CLASE")
print("=" * 60)
print()

survival_class = (
    df.groupby("Pclass")["Survived"]
    .mean()
    .mul(100)
)

print(survival_class)
print()

print("=" * 60)
print("ANÁLISIS 4: SUPERVIVENCIA SEGÚN GRUPO DE EDAD")
print("=" * 60)
print()

survival_age = (
    df.groupby("AgeGroup")["Survived"]
    .mean()
    .mul(100)
)

print(survival_age)
print()

print("=" * 60)
print("ANÁLISIS ADICIONAL: VIAJAR SOLO O ACOMPAÑADO")
print("=" * 60)
print()

survival_alone = (
    df.groupby("IsAlone")["Survived"]
    .mean()
    .mul(100)
)

survival_alone.index = [
    "Acompañado" if value == 0 else "Solo"
    for value in survival_alone.index
]

print(survival_alone)
print()

print("=" * 60)
print("ANÁLISIS ADICIONAL: TARIFA Y SUPERVIVENCIA")
print("=" * 60)
print()

fare_survival = (
    df.groupby("Survived")["Fare"]
    .mean()
)

print(fare_survival)
print()

print("=" * 60)
print("GENERANDO VISUALIZACIONES")
print("=" * 60)
print()

sns.set_theme()

plt.figure(figsize=(8, 5))

sns.barplot(
    data=df,
    x="Sex",
    y="Survived"
)

plt.title("Supervivencia según sexo")
plt.xlabel("Sexo")
plt.ylabel("Porcentaje de supervivencia")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "supervivencia_genero.png"
)

plt.close()

plt.figure(figsize=(8, 5))

sns.barplot(
    data=df,
    x="Pclass",
    y="Survived"
)

plt.title("Supervivencia según clase")
plt.xlabel("Clase del pasajero")
plt.ylabel("Porcentaje de supervivencia")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "supervivencia_clase.png"
)

plt.close()

plt.figure(figsize=(9, 5))

sns.barplot(
    data=df,
    x="AgeGroup",
    y="Survived",
    order=[
        "Niño",
        "Joven",
        "Adulto",
        "Adulto mayor"
    ]
)

plt.title("Supervivencia según grupo de edad")
plt.xlabel("Grupo de edad")
plt.ylabel("Porcentaje de supervivencia")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "supervivencia_edad.png"
)

plt.close()

df.to_csv(
    OUTPUT_DIR / "resultados_procesados.csv",
    index=False
)

print("=" * 60)
print("PROYECTO EJECUTADO CORRECTAMENTE")
print("=" * 60)
print()

print("Los resultados fueron guardados en:")
print(OUTPUT_DIR)