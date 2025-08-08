
import helpers
from django.conf import settings
from django.core.management.base import BaseCommand

STATICFILES_VENDOR_DIR = getattr(settings, 'STATICFILES_VENDOR_DIR')

VENDOR_STATICFILES = {
    "flowbite.min.css": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css",
    "flowbite.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js",
    "flowbite.min.js.map": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js.map",
}

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        completed_urls = []
        
        for name, url in VENDOR_STATICFILES.items():
            output_path = STATICFILES_VENDOR_DIR / name
            self.stdout.write(f"Downloading {name} from {url}")
            
            dl_success = helpers.download_to_local(url, output_path)
            if dl_success:
                completed_urls.append(url)
                self.stdout.write(self.style.SUCCESS(f"Downloaded {name} from {url} to {output_path}"))
            else:
                self.style.ERROR(f"Failed to download {name} from {url}")
                
        if set(completed_urls) == set(VENDOR_STATICFILES.values()):
            self.stdout.write(self.style.SUCCESS("All files downloaded successfully"))
        else:
            self.style.WARNING('Some files were not updated successfully!!')