from app import Torneo, app

app.app_context().push()
torneos = Torneo.query.all()
print(f'\n=== Total torneos: {len(torneos)} ===\n')
for t in torneos:
    print(f'{t.id}. {t.nombre}')
    print(f'   Ubicación: {t.ubicacion}')
    print(f'   Fecha: {t.fecha}')
    print(f'   Estado: {t.estado}')
    print()

