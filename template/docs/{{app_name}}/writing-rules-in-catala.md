# Writing Rules In Catala

## What is Catala?

[Catala](https://catala-lang.org/) is a programming language adapted for socio-fiscal legislative purposes. It allows developers to:

- Write rules alongside the legislative text they implement (literate programming)
- Handle complex legal logic including exceptions and edge cases
- Generate executable code (Python, OCaml) from the legislative specification
- Produce human-readable documentation from the same source

## Adding New Rules

1. Create a new `.catala_en` file in `catala/src/` encoding your legislative text and rules.
2. Add a target entry in `catala/clerk.toml` for the new module.
3. Add test assertions in `catala/tests/`.
4. Run `make catala-build` to compile to Python (typechecking happens as part of the build; outputs go to `src/generated/`).
5. Create a new module file in `src/modules/` (see [Module system](#module-system) below).
6. Add Python tests in `tests/`.
