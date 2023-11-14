import tkinter as tk
from tkinter import messagebox

class Livro:
    def __init__(self, titulo, autor, exemplares_disponiveis):
        self.titulo = titulo
        self.autor = autor
        self.exemplares_disponiveis = exemplares_disponiveis
        self.exemplares_emprestados = 0

class CatalogoLivros:
    def __init__(self):
        self.catalogo = []

    def cadastrar_livro(self, livro):
        if livro.exemplares_disponiveis <= 0:
            messagebox.showinfo("Aviso", "A quantidade de exemplares deve ser maior que zero. Livro não cadastrado.")
        else:
            self.catalogo.append(livro)
            messagebox.showinfo("Sucesso", f"Livro '{livro.titulo}' cadastrado com sucesso!")

    def validar_disponibilidade(self, livro, quantidade):
        if quantidade >= 0 and (livro.exemplares_disponiveis - livro.exemplares_emprestados) >= quantidade:
            return True
        else:
            messagebox.showinfo("Aviso", "A quantidade de exemplares disponíveis é insuficiente ou a quantidade solicitada é inválida.")
            return False

    def emprestar_livro(self, livro, quantidade):
        if self.validar_disponibilidade(livro, quantidade):
            livro.exemplares_emprestados += quantidade
            livro.exemplares_disponiveis -= quantidade  
            messagebox.showinfo("Sucesso", f"{quantidade} exemplar(es) do livro '{livro.titulo}' emprestado(s) com sucesso!")
        else:
            messagebox.showinfo("Aviso", "Quantidade solicitada indisponível.")

    def devolver_livro(self, livro, quantidade):
        if quantidade > 0 and quantidade <= livro.exemplares_emprestados:
            livro.exemplares_emprestados -= quantidade
            livro.exemplares_disponiveis += quantidade  
            messagebox.showinfo("Sucesso", f"{quantidade} exemplar(es) do livro '{livro.titulo}' devolvido(s) com sucesso!")
        else:
            messagebox.showinfo("Aviso", "Quantidade inválida para devolução.")

    def pesquisar_livros(self, termo):
        resultados = []
        for livro in self.catalogo:
            if termo.lower() in livro.titulo.lower() or termo.lower() in livro.autor.lower():
                resultados.append(livro)
        return resultados

    def exibir_catalogo(self):
        if self.catalogo:
            catalogo_str = "Catálogo de Livros:\n"
            for i, livro in enumerate(self.catalogo, 1):
                catalogo_str += f"{i}. Título: {livro.titulo}, Autor: {livro.autor}, Disponíveis: {livro.exemplares_disponiveis}\n"
            return catalogo_str
        else:
            return "O catálogo está vazio."

class AplicacaoCatalogo:
    def __init__(self, root):
        self.catalogo = CatalogoLivros()

        self.root = root
        self.root.title("Catálogo de Livros")

        self.menu = tk.Frame(root)
        self.menu.pack()

        self.label_resultado = tk.Text(root, width=100, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.label_resultado.pack()

        self.opcao_var = tk.StringVar()

        self.opcoes = [
            "Cadastrar Livro",
            "Emprestar Livro",
            "Devolver Livro",
            "Pesquisar Livros",
            "Exibir Catálogo",
            "Sair"
        ]

        for i, opcao in enumerate(self.opcoes, 1):
            tk.Radiobutton(self.menu, text=opcao, variable=self.opcao_var, value=str(i)).pack(anchor=tk.W)

        self.button_executar = tk.Button(root, text="Executar", command=self.executar_acao)
        self.button_executar.pack()

    def executar_acao(self):
        opcao = self.opcao_var.get()

        if opcao == "1":
            self.cadastrar_livro()
        elif opcao == "2":
            self.emprestar_livro()
        elif opcao == "3":
            self.devolver_livro()
        elif opcao == "4":
            self.pesquisar_livros()
        elif opcao == "5":
            self.exibir_catalogo()
        elif opcao == "6":
            self.sair()
        else:
            messagebox.showinfo("Aviso", "Opção inválida. Tente novamente.")

    def cadastrar_livro(self):
        cadastrar_janela = tk.Toplevel(self.root)
        cadastrar_janela.title("Cadastrar Livro")

        tk.Label(cadastrar_janela, text="Título:").grid(row=0, column=0, padx=10, pady=10)
        titulo_entry = tk.Entry(cadastrar_janela)
        titulo_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(cadastrar_janela, text="Autor:").grid(row=1, column=0, padx=10, pady=10)
        autor_entry = tk.Entry(cadastrar_janela)
        autor_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(cadastrar_janela, text="Exemplares Disponíveis:").grid(row=2, column=0, padx=10, pady=10)
        exemplares_entry = tk.Entry(cadastrar_janela)
        exemplares_entry.grid(row=2, column=1, padx=10, pady=10)

        cadastrar_button = tk.Button(cadastrar_janela, text="Cadastrar", command=lambda: self.cadastrar_livro_handler(titulo_entry.get(), autor_entry.get(), exemplares_entry.get(), cadastrar_janela))
        cadastrar_button.grid(row=3, columnspan=2, pady=10)

    def cadastrar_livro_handler(self, titulo, autor, exemplares, janela):
        try:
            exemplares = int(exemplares)
            novo_livro = Livro(titulo, autor, exemplares)
            self.catalogo.cadastrar_livro(novo_livro)
            janela.destroy()
        except ValueError:
            messagebox.showinfo("Aviso", "A quantidade de exemplares deve ser um número inteiro.")

    def emprestar_livro(self):
        emprestar_janela = tk.Toplevel(self.root)
        emprestar_janela.title("Emprestar Livro")

        tk.Label(emprestar_janela, text="Termo de Pesquisa (Título ou Autor):").grid(row=0, column=0, padx=10, pady=10)
        termo_entry = tk.Entry(emprestar_janela)
        termo_entry.grid(row=0, column=1, padx=10, pady=10)

        pesquisar_button = tk.Button(emprestar_janela, text="Pesquisar", command=lambda: self.pesquisar_livros_handler(termo_entry.get(), emprestar_janela, "emprestar"))
        pesquisar_button.grid(row=1, columnspan=2, pady=10)

    def devolver_livro(self):
        devolver_janela = tk.Toplevel(self.root)
        devolver_janela.title("Devolver Livro")

        tk.Label(devolver_janela, text="Termo de Pesquisa (Título ou Autor):").grid(row=0, column=0, padx=10, pady=10)
        termo_entry = tk.Entry(devolver_janela)
        termo_entry.grid(row=0, column=1, padx=10, pady=10)

        pesquisar_button = tk.Button(devolver_janela, text="Pesquisar", command=lambda: self.pesquisar_livros_handler(termo_entry.get(), devolver_janela, "devolver"))
        pesquisar_button.grid(row=1, columnspan=2, pady=10)

    def pesquisar_livros_handler(self, termo, janela, acao):
        resultados_pesquisa = self.catalogo.pesquisar_livros(termo)

        if resultados_pesquisa:
            escolher_janela = tk.Toplevel(janela)
            escolher_janela.title(f"Escolher Livro para {acao.capitalize()}")

            for i, livro in enumerate(resultados_pesquisa):
                tk.Label(escolher_janela, text=f"{i + 1}. Título: {livro.titulo}, Autor: {livro.autor}, Disponíveis: {livro.exemplares_disponiveis}").pack()

            escolher_label = tk.Label(escolher_janela, text=f"Escolha o número do livro a ser {acao}:")
            escolher_label.pack()

            escolher_entry = tk.Entry(escolher_janela)
            escolher_entry.pack()

            escolher_button = tk.Button(escolher_janela, text=acao.capitalize(), command=lambda: self.acao_livro_handler(resultados_pesquisa, int(escolher_entry.get()) - 1, acao, escolher_janela))
            escolher_button.pack()

        else:
            messagebox.showinfo("Aviso", "Nenhum livro encontrado.")

    def acao_livro_handler(self, resultados_pesquisa, escolha, acao, janela):
        if 0 <= escolha < len(resultados_pesquisa):
            if acao == "emprestar":
                self.catalogo.emprestar_livro(resultados_pesquisa[escolha], 1)
            elif acao == "devolver":
                self.catalogo.devolver_livro(resultados_pesquisa[escolha], 1)

            janela.destroy()
        else:
            messagebox.showinfo("Aviso", "Escolha inválida.")

    def pesquisar_livros(self):
        pesquisar_janela = tk.Toplevel(self.root)
        pesquisar_janela.title("Pesquisar Livros")

        tk.Label(pesquisar_janela, text="Termo de Pesquisa (Título ou Autor):").grid(row=0, column=0, padx=10, pady=10)
        termo_entry = tk.Entry(pesquisar_janela)
        termo_entry.grid(row=0, column=1, padx=10, pady=10)

        pesquisar_button = tk.Button(pesquisar_janela, text="Pesquisar", command=lambda: self.pesquisar_livros_handler(termo_entry.get(), pesquisar_janela, "pesquisar"))
        pesquisar_button.grid(row=1, columnspan=2, pady=10)

    def exibir_catalogo(self):
        catalogo_str = self.catalogo.exibir_catalogo()
        self.label_resultado.config(state=tk.NORMAL)
        self.label_resultado.delete(1.0, tk.END)
        self.label_resultado.insert(tk.END, catalogo_str)
        self.label_resultado.config(state=tk.DISABLED)

    def sair(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoCatalogo(root)
    root.mainloop()
