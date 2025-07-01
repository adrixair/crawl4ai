from pathlib import Path # Importing Path for file handling
from googleS import run_google_search # Import the function to run Google search

query_list = [
    "Instituto Medico Paulista Santana e próximo ao metrô",
    "SRM Asset JK e Faria Lima",
    "Otmow Itaim, Vila Olimpia e Moema",
    "Convex Power Pinheiros e Vila Madalena",
    "Ludemann Berrini",
    "MedSênior Variados",
    "Cury Construtora Pinheiros",
    "Ultra Academia Variados",
    "Tako WGMI Faria Lima, Itaim, JK e Pinheiros",
    "SPX Faria Lima",
    "Somos Gestão de Ações Coletivas Pinheiros",
    "Multilaser Pinheiros",
    "Exeltis Farmaceutica Berrini",
    "Ocre Capital Pinheiros",
    "Cury Construtora Pinheiros",
    "Brennad Energia Itaim, Faria Lima e Pinheiros",
    "Care Plus Pinheiros",
    "Grupo Carpa Pinheiros"
] 

unique_urls = run_google_search(query_list, lang="pt-br", region="br", num_results=10, advanced=False)

output_file = Path(__file__).parent / ".." / "output" / "google_urls_result_SP2.txt"
output_file.parent.mkdir(parents=True, exist_ok=True)

# Delete the file if it already exists
if output_file.exists():
    output_file.unlink()

with open(output_file, "w") as f:
    for url in unique_urls:
        f.write(url + "\n")
print(f"✅ URLs saved to {output_file}")
