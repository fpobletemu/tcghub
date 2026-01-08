from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///torneos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tu-clave-secreta-super-segura-cambiar-en-produccion'
db = SQLAlchemy(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Modelo de Usuario
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modelo de Torneo
class Torneo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_tienda = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)
    hora = db.Column(db.String(5), nullable=False)  # HH:MM
    fecha = db.Column(db.String(50), nullable=False)
    premio = db.Column(db.String(100))
    tipo_juego = db.Column(db.String(50), nullable=False)  # Pokemon, One Piece, etc
    categoria = db.Column(db.String(20), nullable=False)  # Junior, Senior, Master
    tipo_torneo = db.Column(db.String(30), nullable=False)  # League Cup, League Challenge, Liga Casual, Liga Competitiva
    imagen = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre_tienda': self.nombre_tienda,
            'ubicacion': self.ubicacion,
            'hora': self.hora,
            'fecha': self.fecha,
            'premio': self.premio,
            'tipo_juego': self.tipo_juego,
            'categoria': self.categoria,
            'tipo_torneo': self.tipo_torneo,
            'imagen': self.imagen
        }

def crear_torneos_dummy():
    from datetime import datetime, timedelta
    
    tiendas = ['Card Shop Madrid', 'Pokemon World Barcelona', 'Trading Zone Valencia', 'One Piece Store Bilbao', 'Game Master Sevilla', 'Card Kingdom Malaga', 'Collector Alicante', 'Gaming Hub Zaragoza', 'TCG Arena Madrid', 'Dragon Shield Barcelona']
    horas = ['10:00', '14:00', '18:00', '11:00', '15:00', '19:00', '12:00', '16:00', '13:00', '17:00']
    premios = ['$100', '$200', '$50', 'Booster Box', 'Cartas Promocionales', '$150', 'Playmat', 'Sleeves', '$75', 'Deck Box']
    tipos_juego = ['Pokemon', 'One Piece', 'Pokemon', 'One Piece', 'Pokemon', 'One Piece', 'Pokemon', 'One Piece', 'Pokemon', 'One Piece']
    categorias = ['Junior', 'Senior', 'Master', 'Junior', 'Senior', 'Master', 'Junior', 'Senior', 'Master', 'Junior']
    tipos_torneo = ['League Cup', 'League Challenge', 'Liga Casual', 'Liga Competitiva', 'League Cup', 'League Challenge', 'Liga Casual', 'Liga Competitiva', 'League Cup', 'League Challenge']
    imagenes = [
        'https://images.unsplash.com/photo-1611068813580-c0fbba03d6cd?w=400',
        'https://images.unsplash.com/photo-1612404730960-5c71577fca11?w=400',
        None,
        'https://images.unsplash.com/photo-1606503153255-59d8b8b82176?w=400',
        None,
        'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400',
        None,
        'https://images.unsplash.com/photo-1621259182978-fbf93132d53d?w=400',
        None,
        None
    ]
    
    hoy = datetime.now()
    fechas = []
    
    # Fechas pasadas (sábados y domingos)
    for i in range(2, 6):
        dias_atras = i * 7
        fecha = hoy - timedelta(days=dias_atras)
        while fecha.weekday() not in [5, 6]:
            fecha -= timedelta(days=1)
        fechas.append(fecha.strftime('%Y-%m-%d'))
    
    # Fechas futuras (sábados y domingos)
    for i in range(1, 7):
        dias_adelante = i * 7
        fecha = hoy + timedelta(days=dias_adelante)
        while fecha.weekday() not in [5, 6]:
            fecha += timedelta(days=1)
        fechas.append(fecha.strftime('%Y-%m-%d'))
    
    # Crear los 10 torneos
    torneos_dummy = [
        Torneo(
            nombre_tienda=tiendas[i],
            ubicacion=tiendas[i].split()[-1],
            hora=horas[i],
            fecha=fechas[i],
            premio=premios[i],
            tipo_juego=tipos_juego[i],
            categoria=categorias[i],
            tipo_torneo=tipos_torneo[i],
            imagen=imagenes[i]
        )
        for i in range(10)
    ]
    
    for torneo in torneos_dummy:
        db.session.add(torneo)
    db.session.commit()

# Crear las tablas
with app.app_context():
    db.create_all()
    
    # Crear usuario admin si no existe
    try:
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin')
            admin.set_password('admin123')  # Cambiar en producción
            db.session.add(admin)
            db.session.commit()
            print('✓ Usuario admin creado (username: admin, password: admin123)')
    except Exception as e:
        print(f'Nota al crear admin: {str(e)}')
    
    # Crear torneos dummy solo si no hay ninguno
    try:
        if Torneo.query.count() == 0:
            crear_torneos_dummy()
            print('✓ Torneos dummy creados exitosamente')
    except Exception as e:
        print(f'Nota: {str(e)}')

@app.route('/')
def index():
    return render_template('index.html', titulo='InterCards TCG Hub')

@app.route('/admin', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return jsonify({'success': True, 'mensaje': 'Login exitoso'})
        else:
            return jsonify({'success': False, 'mensaje': 'Usuario o contraseña incorrectos'}), 401
    
    return render_template('login.html')

@app.route('/admin/panel')
@login_required
def admin_panel():
    return render_template('admin_panel.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# API REST - Leer todos los torneos
@app.route('/api/torneos', methods=['GET'])
def get_torneos():
    torneos = Torneo.query.all()
    return jsonify([torneo.to_dict() for torneo in torneos])

# HTMX - Renderizar grid de torneos
@app.route('/api/filtrar', methods=['GET'])
def filtrar():
    fecha = request.args.get('filtro-fecha', '')
    ubicacion = request.args.get('filtro-ubicacion', '')
    juego = request.args.get('filtro-juego', '')
    
    query = Torneo.query
    
    if fecha:
        query = query.filter_by(fecha=fecha)
    
    if ubicacion:
        query = query.filter_by(ubicacion=ubicacion)
    
    if juego:
        query = query.filter_by(tipo_juego=juego)
    
    torneos = query.all()
    
    if not torneos:
        return '<p class="text-gray-300 text-center py-20 col-span-full">No hay torneos que coincidan con los filtros</p>'
    
    html = ''
    for torneo in torneos:
        fecha_obj = datetime.strptime(torneo.fecha, '%Y-%m-%d')
        hoy = datetime.now()
        
        # Determinar si es próximo o pasado
        es_proximo = fecha_obj.date() >= hoy.date()
        badge_color = 'bg-red-500' if es_proximo else 'bg-gray-400'
        badge_text = 'PROX' if es_proximo else 'PAST'
        
        # Colores según el juego
        juego_colors = {
            'Pokemon': 'from-yellow-400 to-orange-500',
            'One Piece': 'from-blue-400 to-cyan-500',
            'Yu-Gi-Oh': 'from-purple-500 to-pink-500',
            'Magic': 'from-red-500 to-orange-600'
        }
        gradient = juego_colors.get(torneo.tipo_juego, 'from-gray-400 to-gray-600')
        
        # Formatear fecha y hora
        fecha_formato = fecha_obj.strftime('%d %b')
        
        # Botón siempre habilitado
        boton = f'<button onclick="abrirFormulario({torneo.id})" class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-semibold transition-colors">Ver Detalles</button>'
        
        # Determinar imagen o gradiente por defecto
        if torneo.imagen:
            imagen_html = f'<img src="{torneo.imagen}" alt="{torneo.nombre_tienda}" class="w-full h-48 object-cover">'
        else:
            imagen_html = f'''<div class="h-48 bg-gradient-to-br {gradient} flex items-center justify-center relative overflow-hidden">
                    <div class="absolute inset-0 bg-black opacity-0 group-hover:opacity-10 transition-opacity"></div>
                    <svg class="w-24 h-24 text-white opacity-80" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 2a8 8 0 100 16 8 8 0 000-16zM7 9H5V7h2v2zm4 0H9V7h2v2zm4 0h-2V7h2v2z"/>
                    </svg>
                </div>'''
        
        html += f'''<div class="bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden group hover:-translate-y-2">
            <div class="relative">
                <div class="absolute top-3 left-3 z-10 {badge_color} text-white text-xs font-bold px-3 py-1 rounded-full">
                    {badge_text}
                </div>
                {imagen_html}
            </div>
            <div class="p-4">
                <h3 class="text-lg font-bold text-gray-800 mb-2">{torneo.nombre_tienda}</h3>
                <div class="space-y-2 text-sm text-gray-600 mb-3">
                    <div class="flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                        </svg>
                        <span>{torneo.ubicacion}</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                        <span>{fecha_formato} - {torneo.hora}</span>
                    </div>
                </div>
                <div class="flex flex-wrap gap-2 mb-3">
                    <span class="px-2 py-1 bg-orange-100 text-orange-700 text-xs font-semibold rounded">{torneo.tipo_torneo}</span>
                    <span class="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded">{torneo.categoria}</span>
                </div>
                {boton}
            </div>
        </div>'''
    
    return html

# API REST - Crear torneo
@app.route('/api/torneos', methods=['POST'])
@login_required
def crear_torneo():
    try:
        data = request.get_json()
        nuevo_torneo = Torneo(
            nombre_tienda=data['nombre_tienda'],
            ubicacion=data['ubicacion'],
            hora=data['hora'],
            fecha=data['fecha'],
            premio=data.get('premio', ''),
            tipo_juego=data['tipo_juego'],
            categoria=data['categoria'],
            tipo_torneo=data['tipo_torneo'],
            imagen=data.get('imagen') if data.get('imagen') else None
        )
        db.session.add(nuevo_torneo)
        db.session.commit()
        return jsonify({'mensaje': 'Torneo creado exitosamente', 'torneo': nuevo_torneo.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API REST - Actualizar torneo
@app.route('/api/torneos/<int:id>', methods=['PUT'])
@login_required
def actualizar_torneo(id):
    try:
        torneo = Torneo.query.get(id)
        if not torneo:
            return jsonify({'error': 'Torneo no encontrado'}), 404
        
        data = request.get_json()
        torneo.nombre_tienda = data.get('nombre_tienda', torneo.nombre_tienda)
        torneo.ubicacion = data.get('ubicacion', torneo.ubicacion)
        torneo.hora = data.get('hora', torneo.hora)
        torneo.fecha = data.get('fecha', torneo.fecha)
        torneo.premio = data.get('premio', torneo.premio)
        torneo.tipo_juego = data.get('tipo_juego', torneo.tipo_juego)
        torneo.categoria = data.get('categoria', torneo.categoria)
        torneo.tipo_torneo = data.get('tipo_torneo', torneo.tipo_torneo)
        torneo.imagen = data.get('imagen') if data.get('imagen') else None
        
        db.session.commit()
        return jsonify({'mensaje': 'Torneo actualizado exitosamente', 'torneo': torneo.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API REST - Eliminar torneo
@app.route('/api/torneos/<int:id>', methods=['DELETE'])
@login_required
def eliminar_torneo(id):
    try:
        torneo = Torneo.query.get(id)
        if not torneo:
            return jsonify({'error': 'Torneo no encontrado'}), 404
        
        db.session.delete(torneo)
        db.session.commit()
        return jsonify({'mensaje': 'Torneo eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Inicializar base de datos con datos dummy
@app.route('/api/init-dummy', methods=['POST'])
def init_dummy():
    try:
        if Torneo.query.count() > 0:
            return jsonify({'mensaje': 'Ya existen torneos en la base de datos'}), 200
        
        crear_torneos_dummy()
        return jsonify({'mensaje': 'Torneos dummy creados exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
