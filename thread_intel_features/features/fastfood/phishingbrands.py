import os.path as op

import pandas as pd

from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource

df = pd.read_csv(op.join(op.dirname(__file__), 'data', 'phishingbrands.csv'))
df_dict = df.to_dict('records')


class PhishingBrands(MethodResource, Resource):
    # @requires_auth
    def get(self, domain):
        brand = False
        for row in df_dict:
            if str(row['brand']).lower() in str(domain).lower():
                brand = True
                result = row['brand']
                break
        detail = "Found phishing brand in domain: " + str(result) if brand else "Not phishing brand found in domain."
        return jsonify(dict(feature='phishingbrands', domain=domain, result=brand, detail=detail))
