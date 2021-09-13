import numpy as np
import pandas as pd
import os.path as op

from flask import jsonify
from flask_restful import Resource
from flask_apispec.views import MethodResource

df = pd.read_csv(op.join(op.dirname(__file__), 'data', 'ddns.csv'))

class DDns(MethodResource,Resource):
    # @requires_auth
    def get(self, domain):
        r = np.where(df['domain'] == domain)
        try:
            result = False if str(r[0][0]) == '' else True
        except:
            result = False
        detail = "Domain listed as Dynamic DNS" if result else "Domain not listed as Dynamic DNS"
        return jsonify({"feature": "ddns", "domain": domain, "result": result, "detail": detail})
