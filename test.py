#!/usr/bin/python
# -*- coding: UTF-8 -*-
import base64

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


def aes_ecb_encrypt(message, key):
    '''
    use AES CBC to encrypt message, using key and init vector
    :param message: the message to encrypt
    :param key: the secret
    :return: bytes init_vector + encrypted_content
    '''
    iv_len = 16
    assert type(message) in (str,bytes)
    assert type(key) in (str,bytes)
    if type(message) == str:
        message = bytes(message, 'utf-8')
    if type(key) == str:
        key = bytes(key, 'utf-8')
    backend = default_backend()
    # iv = os.urandom(iv_len)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message) + padder.finalize()
    enc_content = encryptor.update(padded_data) + encryptor.finalize()
    return enc_content

def aes_ecb_decrypt(content, key):
    '''
    use AES CBC to decrypt message, using key
    :param content: the encrypted content using the above protocol
    :param key: the secret
    :return: decrypted bytes
    '''
    assert type(content) == bytes
    assert type(key) in (bytes, str)
    if type(key) == str:
        key = bytes(key, 'utf-8')
    iv_len = 0
    assert len(content) >= (iv_len + 16)
    enc_content = content[iv_len:]
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    unpadder = padding.PKCS7(128).unpadder()
    decryptor = cipher.decryptor()
    dec_content = decryptor.update(enc_content) + decryptor.finalize()
    real_content = unpadder.update(dec_content) + unpadder.finalize()
    return real_content

rers = '[{"logisticsCode":null,"whCode":null,"slipCode2":null,"storeCode":null,"orderSource":"tmall","orderCode":"40000035150012","sourceOrderCode":"40000035150012","vmiOrderCode":null,"owner":"IT后端测试店铺04","acceptOwners":null,"orderType":21,"warehouseCode":"TEST002","planOutboundTime":null,"planArriveTime":null,"memo":"","codAmt":0,"orderAmt":299.00,"orderDiscount":0.00,"freight":0,"orderCreateTime":1506792745000,"convenienceStore":null,"activeCode":null,"country":"中国","province":"上海","province1":null,"city":"上海市","city1":null,"district":"长宁区","district1":null,"address":"云立方B栋","address1":null,"telephone":null,"moblie":"18888888888","receiver":"某某","receiver1":null,"zipcode":"200000","orderUserMail":"zan.ma@baozun.com","orderUserCode":null,"transCode":"STO","transNo":null,"transTimeType":1,"transType":1,"transMemo":"","payments":null,"invoices":null,"packingList":null,"lines":[{"lineNo":"1000001686","sku":"[TEST]3Z54qy_185-i205185-10","qty":1,"vasList":null,"skuName":"IT后端测试店铺04","listPrice":1.00,"unitPrice":1.00,"lineDiscount":0,"lineAmt":1.00,"activeCode":null,"owner":"IT后端测试店铺04","warehouseCode":null,"invStatus":"良品","ext_code":null,"sns":null,"origin":null,"batchNo":null,"sExpDate":null,"eExpDate":null,"fullLineOutbound":null,"partOutboundStrategy":null,"invType":null,"invAttr1":null,"invAttr2":null,"invAttr3":null,"invAttr4":null,"invAttr5":null,"outboundCartonType":null,"wmsOutBoundSnLines":null,"mixingAttr":null,"platformOrderLineCode":"50013326","picPath":null,"isCommon":null,"orderLineType":1,"barCode":"[TEST]3Z54qy_185-i205185-10","keyProp":null,"supplierCode":null,"comboCode":"COMB003797","extensionCode2":"[TEST]3Z54qy_185-i205185-10","gift":false}],"vasList":null,"orderSourcePlatform":"TM","systemName":null,"customerCode":"CUS_BAOZUN","odoType":"2","extOdoType":"21","partOutboundStrategy":null,"qty":1.0,"epistaticSystemsOrderType":null,"outboundCartonType":null,"includeHazardousCargo":false,"includeFragileCargo":false,"insuranceCoverage":null,"isWholeOrderOutbound":true,"crossDockingSymbol":null,"distributionTargetVillagesTowns":null,"distributionTargetEmail":null,"consigneeTargetMobilePhone":null,"consigneeTargetTelephone":null,"consigneeTargetCountry":null,"consigneeTargetProvince":null,"consigneeTargetCity":null,"consigneeTargetDistrict":null,"consigneeTargetVillagesTowns":null,"consigneeTargetAddress":null,"consigneeTargetEmail":null,"consigneeTargetZip":null,"isPermitOutBound":true,"ecOrderType":"0","platformPaymentTime":null,"platformCreateTime":1506792745000,"totalQty":null,"deliveryType":0,"remark":null,"vipCard":null,"platformMemberCode":"libbuct2002","isPreSale":"0","transBigWord":null,"packageCenterCode":null,"expressType":null,"ifStoreCollect":false,"o2oShopCode":null,"toWhTime":null,"transUpgrade":false,"cod":false,"codPos":false,"allowDS":false,"allowDSL":false,"dslocked":false,"locked":false}]'
encrypt = aes_ecb_encrypt(bytes(rers, encoding='utf-8'), "fe74316914745ab7")
print(encrypt)

dfd = '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'
decrypt = aes_ecb_decrypt(encrypt, "fe74316914745ab7")
encodestr = base64.b64encode(encrypt)
decode = base64.b64decode(dfd)
print(decode)
print(encodestr)
print(decrypt.decode('utf-8'))
