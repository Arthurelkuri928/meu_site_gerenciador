from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from src.models.user import db, User
from werkzeug.security import generate_password_hash # Already in user.py but good for clarity

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('serve')) # Redirect to home or dashboard if already logged in
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin_form = request.form.get('is_admin') # Expect 'on' or None

        if not username or not password:
            flash('Nome de usuário e senha são obrigatórios.', 'danger')
            return redirect(url_for('auth_bp.register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Este nome de usuário já existe. Escolha outro.', 'warning')
            return redirect(url_for('auth_bp.register'))

        new_user = User(username=username)
        new_user.set_password(password)
        if is_admin_form == 'on': # Check if the admin checkbox was checked
            # For initial setup, the first registered user could be made admin
            # Or have a specific registration key for admins
            # For now, let's allow creating an admin via form for simplicity during dev
            # In a real app, this would be more secure (e.g., only first user or via CLI)
            if not User.query.filter_by(is_admin=True).first(): # Make first user admin if no admin exists
                 new_user.is_admin = True
            elif current_user.is_authenticated and current_user.is_admin: # Allow admin to create other admins
                 new_user.is_admin = True
            # else: # Non-admin users cannot create admin accounts by default
            #    flash('Você não tem permissão para criar uma conta de administrador.', 'danger')
            #    return redirect(url_for('auth_bp.register'))

        db.session.add(new_user)
        db.session.commit()
        flash('Registro bem-sucedido! Faça o login.', 'success')
        return redirect(url_for('auth_bp.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('serve')) # Redirect to home or dashboard
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login bem-sucedido!', 'success')
            # Redirect to a dashboard or home page after login
            # For now, redirecting to the main page served by 'serve'
            # Later, we can redirect to a specific dashboard: url_for('admin_bp.dashboard') if user.is_admin else url_for('user_bp.dashboard')
            return redirect(url_for('serve')) 
        else:
            flash('Nome de usuário ou senha inválidos.', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth_bp.login'))

