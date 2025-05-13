from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from src.models.user import db # db is initialized in models/user.py
from src.models.config import SiteConfiguration # Import the SiteConfiguration model

admin_bp = Blueprint(\'admin_bp\', __name__)

def get_config_value(key, default=None):
    config = SiteConfiguration.query.filter_by(key=key).first()
    return config.value if config else default

def set_config_value(key, value):
    config = SiteConfiguration.query.filter_by(key=key).first()
    if config:
        config.value = value
    else:
        config = SiteConfiguration(key=key, value=value)
        db.session.add(config)
    db.session.commit()

@admin_bp.route(\'/panel\')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash("Acesso negado. Você não tem permissão para acessar esta página.", "danger")
        return redirect(url_for(\'dashboard\'))
    
    site_title = get_config_value(\'site_title\', default=\'Meu Site Padrão - Config DB\')
    return render_template(\'admin_panel.html\', site_title=site_title)

@admin_bp.route(\'/settings\', methods=[\'GET\', \'POST\'])
@login_required
def manage_settings():
    if not current_user.is_admin:
        flash("Acesso negado.", "danger")
        return redirect(url_for(\'dashboard\'))

    if request.method == \'POST\':
        new_site_title = request.form.get(\'site_title\')
        set_config_value(\'site_title\', new_site_title)
        flash(f"Título do site atualizado para: {new_site_title}", "success")
        return redirect(url_for(\'admin_bp.admin_panel\'))

    current_site_title = get_config_value(\'site_title\', default=\'Meu Site Padrão - Config DB\')
    return render_template(\'manage_settings.html\', current_site_title=current_site_title)

@admin_bp.route(\'/users\')
@login_required
def manage_users():
    if not current_user.is_admin:
        flash("Acesso negado.", "danger")
        return redirect(url_for(\'dashboard\'))
    # Add logic to list users, promote/demote users, etc.
    # This is a placeholder for now.
    from src.models.user import User # Import User model here to avoid circular dependency if User model imports something from admin routes
    users = User.query.all()
    return render_template(\'manage_users.html\', users=users)

@admin_bp.route(\'/user/<int:user_id>/toggle_admin\', methods=[\'POST\'])
@login_required
def toggle_admin_status(user_id):
    if not current_user.is_admin:
        flash("Acesso negado.", "danger")
        return redirect(url_for(\'dashboard\'))

    from src.models.user import User
    user_to_modify = User.query.get_or_404(user_id)

    if user_to_modify.id == current_user.id and user_to_modify.is_admin:
        # Prevent admin from removing their own admin status if they are the only admin
        admin_count = User.query.filter_by(is_admin=True).count()
        if admin_count <= 1:
            flash("Não é possível remover o status de administrador do único administrador.", "warning")
            return redirect(url_for(\'admin_bp.manage_users\'))

    user_to_modify.is_admin = not user_to_modify.is_admin
    db.session.commit()
    status = "promovido a" if user_to_modify.is_admin else "rebaixado de"
    flash(f"Usuário {user_to_modify.username} {status} administrador.", "success")
    return redirect(url_for(\'admin_bp.manage_users\'))

