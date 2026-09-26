import requests

def analisar_site(url):
    resultado = {
        "possui_site": False,
        "site_funcionando": False,
        "https": False,
        "mobile": False
    }
    
    if not url:
        return resultado
        
    resultado["possui_site"] = True
    if url.startswith("https://"):
        resultado["https"] = True
        
    formatted_url = url if url.startswith("http") else f"http://{url}"
    
    try:
        response = requests.get(formatted_url, timeout=5)
        if response.status_code < 400:
            resultado["site_funcionando"] = True
            if "viewport" in response.text.lower():
                resultado["mobile"] = True
    except:
        resultado["site_funcionando"] = False
        
    return resultado

def analisar_redes_sociais(instagram):
    return bool(instagram and instagram.strip() != "")
