import json
from forta_agent import Finding, FindingType, FindingSeverity, get_json_rpc_url
from web3 import Web3
from src.constants import CTOKEN_CONTRACTS, ABI, TIME_WINDOW, UTILIZATION_RATE_TH


class UtilizationRate:
    def __init__(self, token):
        self.token = token
        self.rates = []

    def add_rate(self, rate, timestamp):
        self.rates.append(RateTimestamped(rate, timestamp))

    def analyze(self):
        self.rates = list(
            filter(lambda x: x.timestamp + TIME_WINDOW > max([z.timestamp for z in self.rates]), self.rates))
        dif = max([x.rate for x in self.rates]) - min([x.rate for x in self.rates])
        if dif > UTILIZATION_RATE_TH:
            return True, dif
        return False, dif


class RateTimestamped:
    def __init__(self, rate, timestamp):
        self.rate = rate
        self.timestamp = timestamp


def get_utilization_rate(ctoken_address, block_number):
    contract = web3.eth.contract(address=Web3.toChecksumAddress(ctoken_address), abi=abi)
    total_borrows_current = contract.functions.totalBorrowsCurrent().call(
        block_identifier=int(block_number))
    cash = contract.functions.getCash().call(block_identifier=int(block_number))
    ur = total_borrows_current / (cash + total_borrows_current)
    return ur


def get_severity(dif):
    if 0.1 <= dif < 0.15:
        return FindingSeverity.Medium
    elif 0.15 <= dif < 0.2:
        return FindingSeverity.High
    elif dif >= 0.2:
        return FindingSeverity.Critical
    else:
        return FindingSeverity.Info


def provide_handle_block(_):
    def handle_block(block_event):
        findings = []

        for ctoken_name, ctoken_address in CTOKEN_CONTRACTS.items():

            ur = get_utilization_rate(ctoken_address, block_event.block_number)
            token_rates[ctoken_name].add_rate(ur, block_event.block.timestamp)
            changed, dif = token_rates[ctoken_name].analyze()

            if changed:
                findings.append(Finding({
                    'name': 'CToken Utilization Rate Significantly Changed',
                    'description': f'cToken {ctoken_name} Utilization Rate changed for {dif}',
                    'alert_id': f'{ctoken_name.capitalize()}_UT_RATE_ALERT',
                    'type': FindingType.Suspicious,
                    'severity': get_severity(dif),
                    'metadata': {
                        'timestamp': block_event.block.timestamp,
                        'utilization_rate': ur,
                        'difference': dif,
                    }
                }))

        return findings

    return handle_block


def handle_block(block_event):
    return real_handle_block(block_event)


web3 = Web3(Web3.HTTPProvider(get_json_rpc_url()))
abi = json.loads(ABI)
token_rates = {}

for token, _ in CTOKEN_CONTRACTS.items():
    token_rates |= {token: UtilizationRate(token)}

real_handle_block = provide_handle_block(web3)
