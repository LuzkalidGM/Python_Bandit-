import ast
import bandit
from bandit.core import issue
from bandit.core import test_properties as test

@test.checks('Call')
@test.test_id('DEMO001')
def detect_database_raw_queries(context):
    """Detecta consultas SQL directas que podrían ser vulnerables a inyección."""
    if context.call_function_name_qual == 'sqlite3.connect' or context.call_function_name == 'connect':
        # Buscar llamadas a execute después de esta conexión
        parent = context.node.parent
        while parent:
            if isinstance(parent, ast.Assign):
                var_name = parent.targets[0].id if hasattr(parent.targets[0], 'id') else None
                if var_name:
                    # Buscar llamadas posteriores usando esta variable
                    for node in ast.walk(context.node.root):
                        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                            if hasattr(node.func.value, 'id') and node.func.value.id == var_name:
                                if node.func.attr == 'execute':
                                    # Verificar si hay una consulta sin parametrizar
                                    if len(node.args) > 0 and isinstance(node.args[0], ast.Str):
                                        query = node.args[0].s
                                        if 'WHERE' in query and ('%s' not in query and '?' not in query):
                                            return bandit.Issue(
                                                severity=bandit.HIGH,
                                                confidence=bandit.MEDIUM,
                                                text="Posible consulta SQL sin parametrizar detectada"
                                            )
            parent = parent.parent
    return None

@test.checks('Call')
@test.test_id('DEMO002')
def detect_weak_crypto(context):
    """Detecta el uso de algoritmos criptográficos débiles."""
    if context.call_function_name_qual == 'hashlib.md5' or context.call_function_name == 'md5':
        return bandit.Issue(
            severity=bandit.MEDIUM,
            confidence=bandit.HIGH,
            text="Uso de MD5 detectado. Este algoritmo no es seguro para usos criptográficos."
        )
    
    if context.call_function_name_qual == 'Crypto.Cipher.DES.new' or context.call_function_name == 'DES':
        return bandit.Issue(
            severity=bandit.HIGH,
            confidence=bandit.HIGH,
            text="Uso del algoritmo DES detectado. DES se considera inseguro, use AES."
        )
    
    return None
