## Descripción
<!-- Describe el cambio realizado y la motivación detrás del mismo -->



## Tipo de cambio
- [ ] 🐛 Bug fix (cambio que soluciona un problema sin romper funcionalidad existente)
- [ ] ✨ Nueva feature (cambio que añade funcionalidad sin romper la existente)
- [ ] 💥 Breaking change (fix o feature que causa que funcionalidad existente deje de funcionar)
- [ ] 🔧 Refactoring (cambio de código que no añade feature ni corrige bug)
- [ ] 📝 Solo documentación
- [ ] 🧪 Solo tests

## Cambios realizados
<!-- Lista los cambios principales realizados en este PR -->
- Cambio 1
- Cambio 2

---

## Checklist de Documentación 📝

> **Regla: "No docs, no merge."** Todo cambio en código público requiere documentación actualizada.

### In-Code Documentation
- [ ] He añadido/actualizado **docstrings Google Style** para todas las funciones/clases nuevas o modificadas
- [ ] Los **type hints** están completos y correctos
- [ ] Los docstrings incluyen secciones: `Args`, `Returns`, `Raises` (donde aplique)
- [ ] He añadido al menos un `Example` en docstrings de funciones complejas
- [ ] `pydocstyle --convention=google` pasa sin errores
- [ ] `interrogate` reporta ≥ 95% de cobertura de docstrings

### Off-Code Documentation
- [ ] He actualizado el **README** si el cambio afecta al uso, instalación o configuración
- [ ] He actualizado el **CHANGELOG.md** bajo la sección `[Unreleased]`
- [ ] `mkdocs build --strict` pasa sin warnings
- [ ] He actualizado el **data dictionary** si hay cambios de schema

### Si es un breaking change
- [ ] He escrito una **guía de migración**
- [ ] He marcado la funcionalidad anterior como `deprecated` con `warnings.warn()`
- [ ] He documentado el timeline de deprecación

---

## Checklist General ✅

- [ ] Mi código sigue los estándares de estilo del proyecto (black, isort, ruff)
- [ ] He escrito tests para los cambios realizados
- [ ] Todos los tests pasan (`pytest`)
- [ ] La cobertura de tests se mantiene ≥ 80%
- [ ] He ejecutado `pre-commit run --all-files` sin errores
- [ ] He revisado mi propio código antes de solicitar review
- [ ] No he incluido credenciales, tokens ni datos sensibles

---

## Screenshots / Output (si aplica)
<!-- Añade capturas de pantalla o output relevante -->

## Notas para el reviewer
<!-- Cualquier contexto adicional que ayude en la revisión -->

