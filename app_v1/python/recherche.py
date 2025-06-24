from pathlib import Path # Importing Path for file handling
from googleS import run_google_search # Import the function to run Google search

query_list = [
    "arquiteto sao paulo",
    "incorporadora sao paulo",
    "arquitetura residencial São Paulo",
    "arquitetura luxo sao paulo",
    "arquiteto hospitalar de alto padrão sao paulo",
    "arquitetura residencial São Paulo de alto padrão",
    "arquitetura residencial de luxo sao paulo",
    "condomínio de luxo sao paulo",
    "criação de alto padrão sao paulo",
    "site de arquiteto São Paulo",
    "arquiteto interiores São Paulo",
    "arquitetos comerciais São Paulo",
    "incorporadora residencial São Paulo",
    "top incorporadoras SP"
]  

unique_urls = run_google_search(query_list, lang="pt-br", region="br", num_results=100, advanced=False)

output_file = Path(__file__).parent / ".." / "output" / "google_urls_result_SP.txt"
output_file.parent.mkdir(parents=True, exist_ok=True)

# Delete the file if it already exists
if output_file.exists():
    output_file.unlink()

with open(output_file, "w") as f:
    for url in unique_urls:
        f.write(url + "\n")
print(f"✅ URLs saved to {output_file}")
