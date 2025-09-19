import os
from django.core.management.base import BaseCommand
from django.conf import settings
from movie.models import Movie  # 👈 ajusta si tu modelo tiene otro nombre

class Command(BaseCommand):
    help = "Asigna imágenes a las películas usando los archivos en media/movie/images/"

    def handle(self, *args, **kwargs):
        images_folder = os.path.join(settings.MEDIA_ROOT, "movie", "images")
        if not os.path.exists(images_folder):
            self.stdout.write(self.style.ERROR(f"No se encontró la carpeta: {images_folder}"))
            return

        updated = 0
        for movie in Movie.objects.all():
            # Busca un archivo que coincida con el nombre de la película
            for ext in [".jpg", ".jpeg", ".png", ".webp"]:
                image_path = os.path.join(images_folder, f"{movie.title}{ext}")
                if os.path.exists(image_path):
                    movie.image = f"movie/images/{movie.title}{ext}"
                    movie.save()
                    updated += 1
                    self.stdout.write(self.style.SUCCESS(f"✅ Imagen asignada a: {movie.title}"))
                    break  # pasa a la siguiente película si ya encontró imagen

        self.stdout.write(self.style.SUCCESS(f"Total de películas actualizadas: {updated}"))
