import os
import requests
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv


class Command(BaseCommand):
    help = "Genera imágenes para las películas usando la API de OpenAI"

    def handle(self, *args, **kwargs):
        # ✅ Cargar variables de entorno
        load_dotenv('../openAI.env')

        # ✅ Inicializar cliente de OpenAI
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        # ✅ Crear carpeta de imágenes si no existe
        images_folder = 'media/movie/images/'
        os.makedirs(images_folder, exist_ok=True)

        # ✅ Consultar películas en la base de datos
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        # ✅ Procesar solo la primera película (por ahora)
        for movie in movies:
            image_relative_path = self.generate_and_download_image(client, movie.title, images_folder)
            movie.image = image_relative_path
            movie.save()
            self.stdout.write(self.style.SUCCESS(f"Saved and updated image for: {movie.title}"))
            break  # ⚠️ NO quitar el break todavía

    # ✅ Función auxiliar bien indentada
    def generate_and_download_image(self, client, movie_title, save_folder):
    prompt = f"Movie poster of {movie_title}"
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="256x256",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url

    image_filename = f"m_{movie_title}.png"
    image_path_full = os.path.join(save_folder, image_filename)

    image_response = requests.get(image_url)
    image_response.raise_for_status()
    with open(image_path_full, 'wb') as f:
        f.write(image_response.content)

    return os.path.join('movie/images', image_filename)
