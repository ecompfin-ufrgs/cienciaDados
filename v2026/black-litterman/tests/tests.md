# Testes

Os testes automatizados usam `pytest`, ficam em arquivos `test_*.py` e não acessam a rede.

## Modelo

| ID | Teste | Resultado esperado | Requisito |
|---|---|---|---|
| T-01 | Exemplo publicado | Reproduz Π, `μ_BL` e pesos com erro ≤ 1e-4 | RNF-05 |
| T-02 | Sem views | `μ_BL = Π`; sem restrições, `w* = w_mkt` | FR-MOD-09 |
| T-03 | Ω próximo de zero | `P · μ_BL = Q` | FR-MOD-08 |
| T-04 | View neutra (`Q = PΠ`) | `μ_BL = Π` | FR-MOD-08 |
| T-05 | Ω muito grande | `μ_BL` converge para Π | FR-MOD-08 |
| T-06 | Ativos em outra ordem | Mesmos pesos, reordenados | FR-MOD-06 |
| T-07 | Views inválidas | Duplicadas ou dependentes geram `InvalidViewError` | FR-MOD-06 |
| T-08 | Restrições | Pesos somam 1, `w ≥ 0` e nenhum passa de 20% | FR-MOD-10 |
| T-09 | Problema inviável | Gera `InfeasibleOptimizationError` | FR-MOD-13 |

## Dados

| ID | Teste | Resultado esperado | Requisito |
|---|---|---|---|
| T-10 | Dados faltantes | Forward-fill não passa de 5 dias; ativo sem cobertura sai com aviso | FR-TRA-02 |
| T-11 | Excesso de retorno | `r_ex + r_f = r` | FR-TRA-04 |
| T-12 | Covariância | Σ simétrica, PSD e anualizada corretamente | FR-TRA-05 |

## Backtest

| ID | Teste | Resultado esperado | Requisito |
|---|---|---|---|
| T-13 | Look-ahead | Pesos em `t` não mudam com dados posteriores a `t` | FR-BKT-01 |

## Backend

| ID | Teste | Resultado esperado | Requisito |
|---|---|---|---|
| T-14 | Recorte do snapshot | Σ e `w_mkt` correspondem aos ativos escolhidos | FR-API-02 |
| T-15 | Snapshot ausente | API devolve `SNAPSHOT_UNAVAILABLE` (503) | FR-COL-08 |
| T-16 | Carteira pela API | Requisição válida devolve pesos e data dos dados | FR-API-02 |
| T-17 | Desempenho | Cálculo da carteira em menos de 2 s | RNF-07 |
