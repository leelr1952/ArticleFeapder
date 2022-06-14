import hashlib
from codecs import encode
from selectolax.parser import HTMLParser


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def genlistpayload(searchword):
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=searchword;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(searchword))
    dataList.append(encode('--' + boundary + '--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    return payload


def genpayload(searchword, page_num):
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList = []
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=page;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(str(page_num)))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=searchword;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    # dataList.append(encode("T_L CTITLE T_D E_KEYWORDS T_JT_E T_L纪要 T_R  and cchannelcode T_E T_L0T_D8349T_D9862T_D9860T_D12002T_D8361T_D9867T_D11795T_D9858T_D8320T_D9865T_D8319T_D9868T_D8875T_D8415T_D12635T_D10743T_D9857T_D10007T_D10012T_D10037T_D10008T_D10744T_D8774T_D9866T_D12008T_D8661T_D8367T_D8458T_D10058T_D8853T_D8432T_D12698T_D11794T_D8834T_D8883T_D10009T_D8876T_D8614T_D10053T_D8884T_D8329T_D9859T_D8804T_D12430T_D8324T_D8999T_D8737T_D12369T_D8660T_D8762T_D13129T_D13061T_D10978T_D13176T_D8414T_D11796T_D9861T_D8369T_D11904T_D8857T_D11837T_D8325T_D8960T_D8767T_D12431T_D8858T_D12092T_D8859T_D9892T_D10005T_D9891T_D12053T_D8368T_D10055T_D8649T_D12695T_D10052T_D13174T_D8345T_D10976T_D12705T_D13236T_D8322T_D8629T_D10054T_D8719T_D9394T_D8344T_D8326T_D13184T_D8654T_D12789T_D8697T_D8772T_D8860T_D12094T_D8696T_D13179T_D8838T_D11898T_D8630T_D8765T_D8766T_D8819T_D8711T_D9004T_D8691T_D8769T_D8882T_D8533T_D8651T_D8690T_D8943T_D9002T_D9895T_D8341T_D8826T_D8861T_D9869T_D12095T_D12796T_D8902T_D12812T_D10022T_D11601T_D12166T_D12780T_D8334T_D12774T_D8346T_D8720T_D9000T_D9091T_D13246T_D8647T_D8652T_D8656T_D9001T_D8763T_D12169T_D12788T_D12794T_D13140T_D8650T_D8657T_D8689T_D8750T_D8942T_D8998T_D11901T_D12163T_D8373T_D8551T_D9348T_D13186T_D8644T_D8646T_D8903T_D11867T_D8642T_D8693T_D8773T_D8885T_D11590T_D11899T_D11948T_D12792T_D13181T_D8347T_D8400T_D8447T_D8771T_D8786T_D8552T_D8645T_D8944T_D11949T_D12783T_D8658T_D8694T_D8741T_D9863T_D11900T_D12091T_D12701T_D8698T_D8700T_D10833T_D12806T_D8598T_D8701T_D8964T_D11749T_D11855T_D12399T_D12470T_D12775T_D12776T_D12779T_D12809T_D13182T_D8385T_D8751T_D8768T_D8946T_D11853T_D11978T_D12632T_D12786T_D12807T_D8643T_D8655T_D8820T_D8909T_D10858T_D10957T_D12784T_D12791T_D12803T_D13141T_D8585T_D8597T_D8702T_D8752T_D8798T_D8831T_D8855T_D8945T_D8985T_D8987T_D9347T_D11976T_D12181T_D12798T_D12801T_D12811T_D8317T_D8391T_D8782T_D8872T_D8981T_D9397T_D11750T_D11856T_D11979T_D11981T_D11985T_D12781T_D12787T_D12793T_D12799T_D12800T_D12903T_D13245T_D8357T_D8618T_D8632T_D8787T_D8788T_D8878T_D8904T_D8963T_D9031T_D10029T_D10574T_D10799T_D11359T_D11360T_D11407T_D11751T_D11852T_D11946T_D11953T_D12365T_D12810T_D13180T_D13183T_D8460T_D8608T_D8699T_D8759T_D8797T_D8806T_D8830T_D8870T_D8906T_D8908T_D8912T_D8913T_D8947T_D8957T_D8959T_D9706T_D9796T_D9896T_D10603T_D10868T_D10958T_D10960T_D10964T_D10966T_D10967T_D11109T_D11705T_D11793T_D11947T_D11952T_D11984T_D12471T_D12771T_D12802T_D12804T_D12942T_D12943T_D8358T_D8412T_D8431T_D8599T_D8602T_D8606T_D8723T_D8724T_D8756T_D8758T_D8799T_D8800T_D8801T_D8837T_D8854T_D8869T_D8873T_D8931T_D8933T_D8934T_D8935T_D8936T_D8937T_D8938T_D8939T_D8940T_D8941T_D8955T_D8980T_D8986T_D8995T_D9671T_D9725T_D9900T_D88888888T_DT_RT_R"))
    dataList.append(encode(searchword))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=perpage;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("10"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=orderby;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("-CRELEASETIME"))
    dataList.append(encode('--' + boundary + '--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    print(payload)
    return payload

def parse_html(content):
    tree = HTMLParser(content)

    if tree.body is None:
        return None

    for tag in tree.css('script'):
        tag.decompose()
    for tag in tree.css('style'):
        tag.decompose()

    text = tree.body.text(separator='\n')
    return text
