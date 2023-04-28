from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

with open('archivos.json','r') as libros:
    data = json.load(libros)
    #print(type(data)) dont dorget :3

# Aqui se regresa el index.html por GET
@app.route('/', methods = ['GET'])
def home():
    return render_template('index.html')

# Aqui se regresa todos los libros por GET
@app.route('/libros', methods = ['GET'])
def libreria():
    return jsonify(data)

# Aqui se regresa un libro con un ID espesifico por GET
@app.route('/libros/<int:id>', methods = ['GET'])
def libroID(id):
    for book in data:
        if book['id'] == id:
            return jsonify(book)

# Aqui se crea un nuevo libro por el metodo POST
@app.route('/libros', methods = ['POST'])
def newBook():
    if request.json['name'] != '' and request.json['author'] != '' and request.json['year'] != '':
        # Se crea un diccioonario para agregar el libro en book
        book = {
            'id': len(data)+1,
            'name': request.json['name'],
            'author': request.json['author'],
            'year': request.json['year'],
        }
        data.append(book) # Agregamos el nueo libro book
        # Modificamos el archivo Json para subir el nuevo book
        with open('archivos.json', 'w') as new_book:
            json.dump(data,new_book,indent=4)
    return jsonify(data)

# Aqui se elimina un libro usando un ID con el metodo DELETE
@app.route('/libros/<int:id>', methods = ['DELETE'])
def deleteBook(id):
    borra = None
    for book in data:
        if book['id'] == id:
            borra = book
    if book is not None:
        data.remove(borra)
        with open('archivos.json', 'w') as borra_book:
            json.dump(data,borra_book,indent=4)
        return jsonify({"message":"Libro borrado"})
    else:
        return jsonify({"message":"Libro no encontrado"})

# Aqui se actualiza un libro usando un ID con el metodo PUT
@app.route('/libros/<int:id>', methods = ['PUT'])
def updateBook(id):
    for book in data:
        if book['id'] == id:
            book['name'] = request.json.get('name', book['name'])
            book['author'] = request.json.get('author', book['author'])
            book['year'] = request.json.get('year', book['year'])

            with open('archivos.json', 'w') as update_book:
                json.dump(data, update_book, indent=4)
            return jsonify(book)

    return jsonify({"message": "Libro no encontrado"})

if __name__ == '__main__':
    app.run(debug=True)

#se actualizó el flask