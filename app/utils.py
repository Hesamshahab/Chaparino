import pandas as pd
from .templates import ChaparinoTemplates

def process_bulk_dispatch(file_content, provider_func, template_name, **static_kwargs):
    # خواندن فایل (CSV یا Excel)
    try:
        df = pd.read_csv(file_content)
    except:
        df = pd.read_excel(file_content)

    results = []
    for _, row in df.iterrows():
        # تبدیل سطر به دیکشنری برای جایگذاری در تمپلیت
        row_data = row.to_dict()
        message = ChaparinoTemplates.render(template_name, **row_data, **static_kwargs)
        
        # فرض بر اینکه ستونی به نام phone در فایل وجود دارد
        status = provider_func(str(row['phone']), message)
        results.append({"phone": row['phone'], "status": "sent", "response": status})
    
    return results