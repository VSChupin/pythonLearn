def city_format(country, city, population=''):
    
    if population:
        
        format_name = f"{country.title()}, {city.title()} - population {population}" 
    else: 
        format_name = f"{country.title()}, {city.title()}"
    
    return format_name