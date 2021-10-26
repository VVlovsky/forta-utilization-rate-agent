# Forta cToken Utilization Rate Agent

## Description

This agent provides alert for 10% or more change in Utilization Rate within a 60-minute window in a given pool.

## Supported Chains

- Ethereum

## Alerts

Describe each of the type of alerts fired by this agent

- CAAVE_UT_RATE_ALERT
- CBAT_UT_RATE_ALERT
- CCOMP_UT_RATE_ALERT
- CDAI_UT_RATE_ALERT
- CETH_UT_RATE_ALERT
- CLINK_UT_RATE_ALERT
- CMKR_UT_RATE_ALERT
- CREP_UT_RATE_ALERT
- CSAI_UT_RATE_ALERT
- CSUSHI_UT_RATE_ALERT
- CTUSD_UT_RATE_ALERT
- CUNI_UT_RATE_ALERT
- CUSDC_UT_RATE_ALERT
- CUSDT_UT_RATE_ALERT
- CWBTC_UT_RATE_ALERT
- CWBTC2_UT_RATE_ALERT
- CYFI_UT_RATE_ALERT
- CZRX_UT_RATE_ALERT
  - Fired when there is 10% or more change in Utilization Rate within a 60-minute window
  - Type is set to "suspicious"
  - Severity depends on how big this change is.

## Test Data

The agent behaviour can be verified using 
```bash
npm test
```

## Utilization Rate
According to the Compound Whitepaper:\
$U_a = Borrows_a / (Cash_a + Borrows_a)$