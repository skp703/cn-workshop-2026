# Get Google Earth Engine access

Earth Engine supports application of the workshop methods to a
participant-selected watershed. The reference-data pathway provides the same
analytical sequence using verified records for Difficult Run and Accotink Creek.

In Google Colab, the Earth Engine Python client is already available. You are
setting up access to the service rather than installing desktop software.

## What you need

- A Google account
- A Google Cloud project you can use
- The Earth Engine API enabled for that project
- The project registered for commercial or noncommercial Earth Engine use

For organization-managed accounts, Cloud project creation may require
administrator approval. A personal Google account may also be used for eligible
noncommercial educational work.

## Setup

1. Sign in to the Google account you intend to use.
2. Open the Google Cloud console and create or select a project.
3. Record the **project ID**, which may differ from the project name.
4. Enable the Google Earth Engine API for that project.
5. Register the project at the Earth Engine registration page and choose the
   category that honestly describes your work.
6. Open `00_Readiness_Check.ipynb` in Colab.
7. Enter the project ID when prompted and run the Earth Engine check.

The check authenticates your account, initializes Earth Engine with the project
ID, and asks the service to evaluate a small arithmetic expression. A printed
value of `42` confirms that the notebook can submit Earth Engine requests.

## Project permissions

Earth Engine initialization uses the same project ID that was enabled and
registered above. The signed-in account must have permission to use that
project. Participants using an institution-managed account may wish to confirm
project access with their administrator before the workshop.

## Official references

- Earth Engine access: <https://developers.google.com/earth-engine/guides/access>
- Python authentication and initialization: <https://developers.google.com/earth-engine/guides/auth>
- Earth Engine in Colab: <https://developers.google.com/earth-engine/guides/python_install-colab>
- Noncommercial tiers: <https://developers.google.com/earth-engine/guides/noncommercial_tiers>
