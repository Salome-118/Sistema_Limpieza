"""Rutas principales: inicio, panel (dashboard) e inventario de productos."""
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user

from app import db
from app.models import Producto
from app.forms import ProductoForm

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    """Inventario del usuario. Permite buscar por nombre o categoría."""
    q = request.args.get("q", "").strip()
    consulta = Producto.query.filter_by(user_id=current_user.id)
    if q:
        like = f"%{q}%"
        consulta = consulta.filter(
            db.or_(Producto.nombre.ilike(like), Producto.categoria.ilike(like))
        )
    productos = consulta.order_by(Producto.nombre.asc()).all()
    return render_template("dashboard.html", productos=productos, q=q)


@main_bp.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def producto_nuevo():
    form = ProductoForm()
    if form.validate_on_submit():
        producto = Producto(
            nombre=form.nombre.data,
            marca=form.marca.data,
            categoria=form.categoria.data,
            precio=form.precio.data,
            stock=form.stock.data,
            descripcion=form.descripcion.data,
            user_id=current_user.id,
        )
        db.session.add(producto)
        db.session.commit()
        flash("Producto agregado al inventario.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("producto_form.html", form=form, titulo="Nuevo producto")


@main_bp.route("/productos/<int:producto_id>/editar", methods=["GET", "POST"])
@login_required
def producto_editar(producto_id):
    producto = db.session.get(Producto, producto_id)
    if producto is None or producto.user_id != current_user.id:
        abort(404)
    form = ProductoForm(obj=producto)
    if form.validate_on_submit():
        producto.nombre = form.nombre.data
        producto.marca = form.marca.data
        producto.categoria = form.categoria.data
        producto.precio = form.precio.data
        producto.stock = form.stock.data
        producto.descripcion = form.descripcion.data
        db.session.commit()
        flash("Producto actualizado.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("producto_form.html", form=form, titulo="Editar producto")


@main_bp.route("/productos/<int:producto_id>/eliminar", methods=["POST"])
@login_required
def producto_eliminar(producto_id):
    producto = db.session.get(Producto, producto_id)
    if producto is None or producto.user_id != current_user.id:
        abort(404)
    db.session.delete(producto)
    db.session.commit()
    flash("Producto eliminado del inventario.", "success")
    return redirect(url_for("main.dashboard"))
