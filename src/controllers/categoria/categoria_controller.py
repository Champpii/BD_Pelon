from flask import request, jsonify

class CategoriaController:
    def __init__(self, db, models):
        self.db = db
        self.models = models

    def getDb(self):
        return self.db

    # Crear una nueva categoría
    def post_categoria(self, data):
        nombre_categoria = data.get('nombre_categoria')
        descripcion = data.get('descripcion')
        categoria_padre = data.get('categoria_padre')

        # Validaciones básicas
        if not nombre_categoria:
            return jsonify({"message": "El nombre de la categoría es obligatorio."}), 400

        # Validar si existe la categoría padre si se proporciona
        if categoria_padre:
            categoria_padre_existente = self.models.DIM_CATEGORIA.query.filter_by(categoria_key=categoria_padre).first()
            if not categoria_padre_existente:
                return jsonify({"message": "La categoría padre no existe."}), 404

        # Crear nueva instancia de categoría
        nueva_categoria = self.models.DIM_CATEGORIA(
            nombre_categoria=nombre_categoria,
            descripcion=descripcion,
            categoria_padre=categoria_padre
        )
        try:
            self.getDb().session.add(nueva_categoria)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al crear la categoría: {str(e)}"}), 500

        return jsonify({"message": "Categoría creada exitosamente."}), 201

    # Obtener todas las categorías con jerarquía y paginación
    def get_categorias(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        categorias = self.models.DIM_CATEGORIA.query.paginate(page=page, per_page=per_page, error_out=False)

        if not categorias.items:
            return jsonify({"message": "No hay categorías registradas."}), 404

        return jsonify({
            "categorias": [categoria.to_dict() for categoria in categorias.items],
            "total": categorias.total,
            "pagina_actual": categorias.page,
            "total_paginas": categorias.pages
        }), 200

    # Obtener una categoría por su ID
    def get_categoria_id(self, id):
        categoria = self.models.DIM_CATEGORIA.query.filter_by(categoria_key=id).first()
        if not categoria:
            return jsonify({"message": "Categoría no encontrada por el ID proporcionado."}), 404

        return jsonify({
            "categoria_nombre": categoria.nombre_categoria,
            "descripcion": categoria.descripcion,
            "categoria_padre": categoria.categoria_padre
        }), 200

    # Actualizar una categoría
    def put_categoria(self, id, data):
        categoria = self.models.DIM_CATEGORIA.query.filter_by(categoria_key=id).first()
        if not categoria:
            return jsonify({"message": "Categoría no encontrada para actualizar."}), 404

        nombre_categoria = data.get('nombre_categoria')
        descripcion = data.get('descripcion')
        categoria_padre = data.get('categoria_padre')

        # Validar campos requeridos
        if not nombre_categoria:
            return jsonify({"message": "El nombre de la categoría es obligatorio."}), 400

        # Verificar si la categoría padre es válida
        if categoria_padre and categoria_padre != id:
            categoria_padre_existente = self.models.DIM_CATEGORIA.query.filter_by(categoria_key=categoria_padre).first()
            if not categoria_padre_existente:
                return jsonify({"message": "La categoría padre no existe."}), 404

        # Actualizar valores
        categoria.nombre_categoria = nombre_categoria
        categoria.descripcion = descripcion
        categoria.categoria_padre = categoria_padre

        try:
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al actualizar la categoría: {str(e)}"}), 500

        return jsonify({"message": "Categoría actualizada exitosamente."}), 200

    # Eliminar una categoría
    def delete_categoria(self, id):
        categoria = self.models.DIM_CATEGORIA.query.filter_by(categoria_key=id).first()
        if not categoria:
            return jsonify({"message": "Categoría no encontrada para eliminar."}), 404

        try:
            self.getDb().session.delete(categoria)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al eliminar la categoría: {str(e)}"}), 500

        return jsonify({"message": "Categoría eliminada exitosamente."}), 200
