import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector

class AddProductDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Enter product information:").grid(row=0, columnspan=2)

        self.name_entry = tk.Entry(master)
        self.description_entry = tk.Entry(master)
        self.price_entry = tk.Entry(master)
        self.quantity_entry = tk.Entry(master)
        self.category_id_entry = tk.Entry(master)

        self.name_entry.grid(row=1, column=1)
        self.description_entry.grid(row=2, column=1)
        self.price_entry.grid(row=3, column=1)
        self.quantity_entry.grid(row=4, column=1)
        self.category_id_entry.grid(row=5, column=1)

        tk.Label(master, text="Product Name:").grid(row=1, sticky="e")
        tk.Label(master, text="Product Description:").grid(row=2, sticky="e")
        tk.Label(master, text="Product Price:").grid(row=3, sticky="e")
        tk.Label(master, text="Product Quantity:").grid(row=4, sticky="e")
        tk.Label(master, text="Product Category ID:").grid(row=5, sticky="e")

        return self.name_entry

    def apply(self):
        self.result = (
            self.name_entry.get(),
            self.description_entry.get(),
            float(self.price_entry.get()),
            int(self.quantity_entry.get()),
            int(self.category_id_entry.get())
        )

class ModifyProductDialog(simpledialog.Dialog):
    def __init__(self, parent, product_id):
        self.product_id = product_id
        super().__init__(parent)

    def body(self, master):
        tk.Label(master, text="Enter new product information:").grid(row=0, columnspan=2)

        self.new_name_entry = tk.Entry(master)
        self.new_description_entry = tk.Entry(master)
        self.new_price_entry = tk.Entry(master)
        self.new_quantity_entry = tk.Entry(master)
        self.new_category_id_entry = tk.Entry(master)

        self.new_name_entry.grid(row=1, column=1)
        self.new_description_entry.grid(row=2, column=1)
        self.new_price_entry.grid(row=3, column=1)
        self.new_quantity_entry.grid(row=4, column=1)
        self.new_category_id_entry.grid(row=5, column=1)

        tk.Label(master, text="New Product Name:").grid(row=1, sticky="e")
        tk.Label(master, text="New Product Description:").grid(row=2, sticky="e")
        tk.Label(master, text="New Product Price:").grid(row=3, sticky="e")
        tk.Label(master, text="New Product Quantity:").grid(row=4, sticky="e")
        tk.Label(master, text="New Product Category ID:").grid(row=5, sticky="e")

        return self.new_name_entry

    def apply(self):
        self.result = (
            self.new_name_entry.get(),
            self.new_description_entry.get(),
            float(self.new_price_entry.get()),
            int(self.new_quantity_entry.get()),
            int(self.new_category_id_entry.get())
        )

class ProductManager:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Gestion de stock")
        self.parent.geometry("800x600")
        self.parent.configure(bg="white")

        # Frame pour les boutons d'action
        self.button_frame = tk.Frame(self.parent, bg="white")
        self.button_frame.pack(pady=10)

        # Bouton pour récupérer les produits
        self.fetch_button = tk.Button(self.button_frame, text="Fetch Products", command=self.fetch_products)
        self.fetch_button.grid(row=0, column=0, padx=10, pady=5)

        # Bouton pour ajouter un produit
        self.add_button = tk.Button(self.button_frame, text="Add Product", command=self.add_product)
        self.add_button.grid(row=0, column=1, padx=10, pady=5)

        # Bouton pour supprimer un produit
        self.delete_button = tk.Button(self.button_frame, text="Delete Product", command=self.delete_product)
        self.delete_button.grid(row=0, column=2, padx=10, pady=5)

        # Bouton pour modifier un produit
        self.modify_button = tk.Button(self.button_frame, text="Modify Product", command=self.modify_product)
        self.modify_button.grid(row=0, column=3, padx=10, pady=5)

        # Zone de texte pour afficher les produits
        self.products_text = tk.Text(self.parent, height=20, width=100)
        self.products_text.pack()

    def fetch_products(self):
        try:
            # Connexion à la base de données MySQL
            cnx = mysql.connector.connect(user='root', password='Mounir-1992', host="localhost", database='store')

            # Création d'un curseur pour exécuter des requêtes SQL sur la base de données
            cursor_product = cnx.cursor()

            # Exécuter la requête SQL pour récupérer tous les produits
            cursor_product.execute("SELECT * FROM product")
            products = cursor_product.fetchall()

            # Effacer le contenu précédent
            self.products_text.delete(1.0, tk.END)

            # Afficher les produits dans la zone de texte
            for product in products:
                self.products_text.insert(tk.END, f"{product}\n")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        finally:
            cursor_product.close()
            cnx.close()

    def add_product(self):
        dialog = AddProductDialog(self.parent)
        if dialog.result:
            name, description, price, quantity, category_id = dialog.result
            try:
                # Connexion à la base de données MySQL
                cnx = mysql.connector.connect(user='root', password='Mounir-1992', host="localhost", database='store')

                # Création d'un curseur pour exécuter des requêtes SQL sur la base de données
                cursor_product = cnx.cursor()

                # Exécuter la requête SQL pour ajouter le nouveau produit
                add_product_query = ("INSERT INTO product (name, description, price, quantity, id_category) "
                                     "VALUES (%s, %s, %s, %s, %s)")
                product_data = (name, description, price, quantity, category_id)
                cursor_product.execute(add_product_query, product_data)

                # Valider les modifications dans la base de données
                cnx.commit()
                messagebox.showinfo("Success", "Product added successfully!")

                # Mettre à jour l'affichage des produits
                self.fetch_products()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

            finally:
                cursor_product.close()
                cnx.close()

    def delete_product(self):
        product_id = simpledialog.askinteger("Delete Product", "Enter product ID to delete:")
        if product_id is not None:
            try:
                # Connexion à la base de données MySQL
                cnx = mysql.connector.connect(user='root', password='Mounir-1992', host="localhost", database='store')

                # Création d'un curseur pour exécuter des requêtes SQL sur la base de données
                cursor_product = cnx.cursor()

                # Exécuter la requête SQL pour supprimer le produit sélectionné
                delete_product_query = "DELETE FROM product WHERE id = %s"
                cursor_product.execute(delete_product_query, (product_id,))

                # Valider les modifications dans la base de données
                cnx.commit()
                messagebox.showinfo("Success", "Product deleted successfully!")

                # Mettre à jour l'affichage des produits
                self.fetch_products()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

            finally:
                cursor_product.close()
                cnx.close()

    def modify_product(self):
        product_id = simpledialog.askinteger("Modify Product", "Enter product ID to modify:")
        if product_id is not None:
            dialog = ModifyProductDialog(self.parent, product_id)
            if dialog.result:
                new_name, new_description, new_price, new_quantity, new_category_id = dialog.result
                try:
                    # Connexion à la base de données MySQL
                    cnx = mysql.connector.connect(user='root', password='Mounir-1992', host="localhost", database='store')

                    # Création d'un curseur pour exécuter des requêtes SQL sur la base de données
                    cursor_product = cnx.cursor()

                    # Exécuter la requête SQL pour mettre à jour le produit avec les nouvelles valeurs
                    update_product_query = ("UPDATE product SET name = %s, description = %s, price = %s, quantity = %s, id_category = %s "
                                            "WHERE id = %s")
                    cursor_product.execute(update_product_query, (new_name, new_description, new_price, new_quantity, new_category_id, product_id))
                    cnx.commit()
                    messagebox.showinfo("Success", "Product updated successfully!")

                    # Mettre à jour l'affichage des produits
                    self.fetch_products()

                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

                finally:
                    cursor_product.close()
                    cnx.close()

if __name__ == "__main__":
    window = tk.Tk()
    app = ProductManager(window)
    window.mainloop()
