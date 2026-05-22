# computacao-grafica-python
Conjunto de aulas com demonstrações práticas dos conceitos abordados na disciplina de Computação Gráfica.

### Configurações do ambiente de desenvolvimento


- Ambiente virtual Python (venv) está ativado.

```bash
    python -m venv venv # No Windows

    python3 -m venv venv # No Linux/macOS
```

```bash
    .\venv\Scripts\Activate # No Windows

    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser # No Windows, caso necessite liberar acesso a execução de script no PowerShell 

    source venv/bin/activate  # No Linux/macOS
```

- Todas as dependências estão instaladas.

```bash
    pip install -r requirements.txt

    pip install --upgrade -r requirements.txt
```