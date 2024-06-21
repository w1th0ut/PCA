import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.conf import settings
from .forms import ImageUploadForm
from .models import UploadImage
from sklearn.decomposition import PCA

def pca_reconstruction(image_path, k):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Split image into R, G, B channels
    R, G, B = cv2.split(img)

    # Normalize the color channels
    R, G, B = R / 255.0, G / 255.0, B / 255.0

    # Apply PCA on each channel
    pca_r = PCA(n_components=k)
    reduced_r = pca_r.fit_transform(R)
    recon_r = pca_r.inverse_transform(reduced_r)

    pca_g = PCA(n_components=k)
    reduced_g = pca_g.fit_transform(G)
    recon_g = pca_g.inverse_transform(reduced_g)

    pca_b = PCA(n_components=k)
    reduced_b = pca_b.fit_transform(B)
    recon_b = pca_b.inverse_transform(reduced_b)

    # Merge channels back
    reconstructed_img = cv2.merge((recon_r, recon_g, recon_b))
    reconstructed_img = np.clip(reconstructed_img, 0, 1)

    # Save the reconstructed image
    reconstructed_image_path = os.path.join(settings.MEDIA_ROOT, 'reconstructed.png')
    plt.imsave(reconstructed_image_path, reconstructed_img)

    return reconstructed_image_path

def pca_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            k_value = form.cleaned_data['k_value']
            image_path = os.path.join(settings.MEDIA_ROOT, image_instance.image.name)
            
            # Process the image with PCA
            reconstructed_image_path = pca_reconstruction(image_path, k_value)
            
            return render(request, 'pca_app/result.html', {
                'original_image': image_instance.image.url,
                'reconstructed_image': '/media/reconstructed.png',
                'k_value': k_value,
            })
    else:
        form = ImageUploadForm()
    return render(request, 'pca_app/upload.html', {'form': form})
