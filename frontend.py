import tkinter as tk
from tkinter import ttk
import requests

# Função para manipular a visibilidade dos campos com base no tipo de requisição
def update_fields(event=None):
    method = request_type.get()
    for widget in [label_name_chave, entry_name_chave, label_name, entry_name, label_email, entry_email]:
        widget.grid_remove()
    if method in ["GET", "DELETE", "PATCH"]:
        label_name_chave.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        entry_name_chave.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    if method in ["POST", "PATCH"]:
        label_name.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        entry_name.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        label_email.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        entry_email.grid(row=4, column=1, padx=10, pady=5, sticky="w")

# Função para enviar a requisição HTTP
# Função para enviar a requisição HTTP
def send_request():
    method = request_type.get()
    base_url = "http://127.0.0.1:5000/"  # URL do servidor backend
    result_box.delete("1.0", tk.END)  # Limpar o campo de resultado

    try:
        if method == "GET":
            name = entry_name_chave.get()
            response = requests.get(base_url, params={"name": name})
        elif method == "DELETE":
            name = entry_name_chave.get()
            response = requests.delete(base_url, json={"name": name})
        elif method == "POST":
            name = entry_name.get()
            email = entry_email.get()
            response = requests.post(base_url, json={"name": name, "email": email})
        elif method == "PATCH":
            name_chave = entry_name_chave.get()
            updates = {}
            if entry_name.get():
                updates["name"] = entry_name.get()
            if entry_email.get():
                updates["email"] = entry_email.get()
            response = requests.patch(f"{base_url}?name={name_chave}", json=updates)
        elif method == "OPTIONS":
            response = requests.options(base_url)
            result_box.insert(tk.END, f"Status: {response.status_code}\n")

            # Adicionando uma verificação para o conteúdo da resposta
            result_box.insert(tk.END, f"Response Content: {response.text}\n")  # Exibe o conteúdo bruto da resposta

            # Verifica se a resposta contém JSON
            try:
                response_json = response.json()  # Tenta decodificar como JSON
                methods_supported = response_json.get('methods', [])
                result_box.insert(tk.END, f"Methods Supported: {', '.join(methods_supported)}\n")
                result_box.insert(tk.END, f"Description: {response_json.get('description', '')}\n")
            except ValueError:  # Caso não seja JSON, trate de forma diferente
                result_box.insert(tk.END, "Resposta não em formato JSON.\n")
            return
        else:
            result_box.insert(tk.END, "Método não suportado.")
            return

        # Exibe o resultado no campo de texto para os outros métodos
        try:
            result_box.insert(tk.END, f"Status: {response.status_code}\n{response.json()}")
        except ValueError:
            result_box.insert(tk.END, f"Status: {response.status_code}\nResposta não em formato JSON.")
    except requests.exceptions.RequestException as e:
        result_box.insert(tk.END, f"Erro ao enviar a requisição: {e}")

# Configuração da janela principal
root = tk.Tk()
root.title("Frontend de Requisições HTTP")
root.configure(bg="#f5f5f5")  # Background sutil

# Widgets para os campos e labels
label_title = tk.Label(root, text="Cliente HTTP", font=("Arial", 16, "bold"), bg="#f5f5f5")
label_title.grid(row=0, column=0, columnspan=2, pady=10)

label_request_type = tk.Label(root, text="Tipo de Requisição:", font=("Arial", 10), bg="#f5f5f5")
label_request_type.grid(row=1, column=0, padx=10, pady=5, sticky="e")

request_type = ttk.Combobox(root, values=["GET", "POST", "PATCH", "DELETE", "OPTIONS"], state="readonly", width=15)
request_type.grid(row=1, column=1, padx=10, pady=5, sticky="w")
request_type.bind("<<ComboboxSelected>>", update_fields)
request_type.current(0)

label_name_chave = tk.Label(root, text="Chave (Nome):", font=("Arial", 10), bg="#f5f5f5")
entry_name_chave = tk.Entry(root, font=("Arial", 10))

label_name = tk.Label(root, text="Nome:", font=("Arial", 10), bg="#f5f5f5")
entry_name = tk.Entry(root, font=("Arial", 10))

label_email = tk.Label(root, text="Email:", font=("Arial", 10), bg="#f5f5f5")
entry_email = tk.Entry(root, font=("Arial", 10))

# Botão para enviar a requisição
btn_send = tk.Button(
    root, text="Enviar Requisição", command=send_request,
    font=("Arial", 10, "bold"), bg="#007BFF", fg="white", padx=10, pady=5
)
btn_send.grid(row=5, column=0, columnspan=2, pady=10)

# Campo de resultado
label_result = tk.Label(root, text="Resultado:", font=("Arial", 10, "bold"), bg="#f5f5f5")
label_result.grid(row=6, column=0, sticky="w", padx=10, pady=5)
result_box = tk.Text(root, height=10, width=50, font=("Courier", 10), wrap="word")
result_box.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

# Inicializa os campos com o método selecionado
update_fields()

# Loop principal da aplicação
root.mainloop()
