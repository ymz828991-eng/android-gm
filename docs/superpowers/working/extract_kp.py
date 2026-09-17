# extract_kp.py — 低电log.docx 说话人普查与 KP 消息分离
# 结构事实：消息由 w:br 软换行分隔在超长段落内（非段落分隔）；账号与时间戳间为 \xa0
# 头两种形态：【组名】账号 时间戳 / 裸账号 时间戳（均独占一行，行尾为 h:m:s）
# 用法: python extract_kp.py census   # 普查，人工确认 KP 账号集
#       python extract_kp.py split    # 按 KP_SET 分离写 低电KP提取.txt
import zipfile, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOCX = 'ref/log区/低电log.docx'
OUT  = 'docs/superpowers/working/低电KP提取.txt'
# 普查确证（消息体均为叙述/裁定/检定指令）：洄音识路、萤石眼 为双 KP；
# 洄音=洄音识路 8/27 单日简称；KP=7/26 单日 KP 账号
KP_SET = {'洄音识路', '萤石眼', '洄音', 'KP'}

z = zipfile.ZipFile(DOCX)
xml = z.read('word/document.xml').decode('utf-8')

# 段落级提取：w:t 取文本、w:br 还原为换行，段与段之间也断行
paras = []
for p in re.findall(r'<w:p[ >].*?</w:p>', xml, re.S):
    parts = []
    for m in re.finditer(r'<w:t[^>]*>([^<]*)</w:t>|<w:br[^>]*/>', p):
        parts.append('\n' if m.group(1) is None else m.group(1))
    t = ''.join(parts).replace('\xa0', ' ')
    if t.strip():
        paras.append(t)

# 行级切分（消息粒度）
lines = [ln.strip() for t in paras for ln in t.split('\n') if ln.strip()]

# 头识别三种：【组名】账号 …时间戳（宽松：名字后可有 hp/san 签名等字段，行尾为时间即可）
#          | 裸账号 (日期)时间（严格：仅名+时间，防误伤叙述行）
#          | 裸账号 hp/x san/x [dex/x] …（带签名卡名，正文同行）
hdr_brk = re.compile(r'^【([^】]+)】\s*([^\s【】]+).*\d{1,2}:\d{2}:\d{2}\s*$')
hdr_bar = re.compile(r'^([^\s【】]{1,30})\s+(?:\d{4}/\d{1,2}/\d{1,2}\s+)?\d{1,2}:\d{2}:\d{2}\s*$')
hdr_sig = re.compile(r'^([^\s【】]{1,30})\s+hp\d+(?:[/.]\d+)?\s+san\d+(?:[/.]\d+)?')

def header_name(t):
    m = hdr_brk.match(t)
    if m:
        return m.group(2), True
    m = hdr_bar.match(t)
    if m:
        return m.group(1), False
    m = hdr_sig.match(t)
    if m:
        return m.group(1), False
    return None, False

if sys.argv[1] == 'census':
    census = {}
    for t in lines:
        n, brk = header_name(t)
        if n:
            k = ('【】' if brk else '裸 ') + n
            census[k] = census.get(k, 0) + 1
    for k, v in sorted(census.items(), key=lambda x: -x[1]):
        print(v, k)
    print('total lines:', len(lines))
elif sys.argv[1] == 'split':
    out, keep = [], False
    for t in lines:
        n, _ = header_name(t)
        if n:
            # 裸名变体前缀匹配（如 洄音 → 洄音识路）
            keep = n in KP_SET or any(n and k.startswith(n) for k in KP_SET)
        if keep:
            out.append(t)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print('KP lines:', len(out), 'chars:', sum(map(len, out)))
