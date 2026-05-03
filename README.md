# 🧪 ExpandTesting-2 — QA Automation con Playwright + Python

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-latest-green?logo=playwright)
![Pytest](https://img.shields.io/badge/Pytest-latest-orange?logo=pytest)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue?logo=githubactions)
[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=MiguelZod24_ExpandTesting-2)](https://sonarcloud.io/summary/new_code?id=MiguelZod24_ExpandTesting-2)

> Proyecto de automatización E2E del módulo de **Login** sobre [ExpandTesting](https://practice.expandtesting.com) usando Python + Playwright + Pytest, con pipeline CI/CD en GitHub Actions y análisis de calidad de código con SonarCloud.

---

## 📋 Descripción

Este proyecto automatiza los tests del módulo de Login de la plataforma **ExpandTesting**, una aplicación web diseñada específicamente para practicar automatización de tests.

**App bajo prueba:** [ExpandTesting](https://practice.expandtesting.com)  
**Módulo cubierto:** Login

---

## 🛠️ Stack Técnico

| Categoría | Herramientas |
|-----------|-------------|
| Automatización | Python · Playwright · Pytest |
| Diseño | Page Object Model (POM) |
| CI/CD | GitHub Actions |
| Calidad de código | SonarCloud — Quality Gate integrado |

---

## 📁 Estructura del Proyecto

```
ExpandTesting-2/
├── .github/
│   └── workflows/
│       └── pipeline.yml     # CI/CD: ejecución de tests + SonarCloud
├── pages/
│   └── login_page.py        # POM — módulo Login
├── test/
│   └── test_login.py        # Tests del módulo Login
├── conftest.py              # Fixtures y configuración de Pytest
├── requirements.txt
└── README.md
```

---

## 🚀 Cómo ejecutar localmente

### 1. Clonar el repositorio
```bash
git clone https://github.com/MiguelZod24/ExpandTesting-2.git
cd ExpandTesting-2
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Instalar navegadores de Playwright
```bash
playwright install chromium
```

### 4. Ejecutar los tests
```bash
pytest -v
```

---

## ⚙️ Pipeline CI/CD

El pipeline se ejecuta automáticamente en cada push y puede lanzarse manualmente desde GitHub Actions.

**Pasos del pipeline:**
1. Instalación de dependencias y navegadores
2. Ejecución de todos los tests en modo headless
3. Análisis de calidad de código con SonarCloud (Quality Gate)

---

## 📊 Resultados

- ✅ Pipeline en verde
- ✅ SonarCloud Quality Gate aprobado
- ✅ Page Object Model implementado

---

## 👤 Autor

**Miguel Barrientos**  
QA Automation Engineer — AI-Augmented QA  
[LinkedIn](https://www.linkedin.com/in/miguelbarrientosottolina/) · [GitHub](https://github.com/MiguelZod24)


