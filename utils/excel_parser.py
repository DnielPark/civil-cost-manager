"""
엑셀 파싱 유틸리티 - 단가명세서 엑셀 파일을 파싱하여
DB insert 가능한 형태로 변환한다.

사용 예:
    from utils.excel_parser import parse_unit_price_excel
    result = parse_unit_price_excel('test.xlsx', 'standard')
    print(f"성공: {len(result['success'])}건, 실패: {len(result['errors'])}건")
"""

import pandas as pd
import os

# 표준 칼럼 헤더 (한글 → 영문 매핑)
STANDARD_COLUMNS = {
    '공종명': 'work_name',
    '규격': 'spec',
    '단위': 'unit',
    '단위수량': 'unit_quantity',
    '재료비': 'material_cost',
    '노무비': 'labor_cost',
    '경비': 'expense_cost',
    '비고': 'note',
}


def _normalize_header(df_columns):
    """엑셀 헤더를 표준 칼럼명으로 변환하고 필수 칼럼 존재 여부 확인"""
    header_map = {}
    for col in df_columns:
        col_stripped = str(col).strip()
        if col_stripped in STANDARD_COLUMNS:
            header_map[col] = STANDARD_COLUMNS[col_stripped]

    # 필수 칼럼 확인
    required = ['work_name', 'spec', 'unit']
    missing = [k for k in required if k not in header_map.values()]
    if missing:
        # 원래 한글명으로 변환
        reverse_map = {v: k for k, v in STANDARD_COLUMNS.items()}
        missing_kr = [reverse_map.get(m, m) for m in missing]
        raise ValueError(f'필수 칼럼 누락: {", ".join(missing_kr)}')

    return header_map


def _parse_row_value(value, field_name, default=0):
    """셀 값을 숫자로 변환. 실패 시 None 반환"""
    if pd.isna(value) or str(value).strip() == '':
        return default
    try:
        # 쉼표 제거 (천 단위 구분자)
        cleaned = str(value).replace(',', '').strip()
        return float(cleaned)
    except (ValueError, TypeError):
        return None


def parse_unit_price_excel(file_path: str, cost_type: str = 'standard') -> dict:
    """
    엑셀 파일을 파싱해서 DB insert 가능한 형태로 반환

    Args:
        file_path: 엑셀 파일 경로 (.xlsx)
        cost_type: 단가 유형 (현재는 검증에만 사용, 추후 확장)

    Returns:
        dict: {
            'success': [정상 파싱된 행 리스트],
            'errors': [파싱 실패 행 리스트 {'row': int, 'reason': str}]
        }

    Raises:
        FileNotFoundError: 파일이 존재하지 않을 때
        ValueError: 필수 칼럼이 누락되었을 때
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'파일을 찾을 수 없습니다: {file_path}')

    # 엑셀 읽기 (헤더 1행, 데이터 2행부터)
    df = pd.read_excel(file_path, engine='openpyxl', header=0, dtype=str)

    if df.empty:
        return {'success': [], 'errors': []}

    # 헤더 정규화
    header_map = _normalize_header(df.columns)

    # 파싱 결과
    success = []
    errors = []

    for idx, row in df.iterrows():
        row_num = idx + 2  # 엑셀상 실제 행 번호 (1행=헤더)

        # 필수값 추출
        def _get_raw(field):
            if field not in header_map.values():
                return ''
            for orig_col, eng_col in header_map.items():
                if eng_col == field:
                    val = row.get(orig_col)
                    if pd.isna(val):
                        return ''
                    return str(val).strip()
            return ''

        work_name = _get_raw('work_name')
        spec = _get_raw('spec')
        unit = _get_raw('unit')

        # 빈 행 체크 (공종명이 비었으면 스킵)
        if not work_name:
            continue
        if not work_name:
            continue

        # 필수 필드 검증
        row_errors = []
        if not work_name:
            row_errors.append('공종명 누락')
        if not spec:
            row_errors.append('규격 누락')
        if not unit:
            row_errors.append('단위 누락')

        if row_errors:
            errors.append({'row': row_num, 'reason': ', '.join(row_errors)})
            continue

        # 헬퍼: 칼럼명으로 값 가져오기
        def _get_col_val(col_name):
            for orig_col, eng_col in header_map.items():
                if eng_col == col_name:
                    return str(row.get(orig_col, '')).strip() if pd.notna(row.get(orig_col)) else ''
            return ''

        # 단위수량
        unit_qty_raw = _get_col_val('unit_quantity')
        if unit_qty_raw:
            unit_qty = _parse_row_value(unit_qty_raw, 'unit_quantity', 1.0)
            if unit_qty is None:
                errors.append({'row': row_num, 'reason': '단위수량 형식 오류'})
                continue
        else:
            unit_qty = 1.0

        # 재료비
        mat_raw = _get_col_val('material_cost')
        if mat_raw:
            mat_cost = _parse_row_value(mat_raw, 'material_cost', 0)
            if mat_cost is None:
                errors.append({'row': row_num, 'reason': '재료비 형식 오류'})
                continue
        else:
            mat_cost = 0

        # 노무비
        lab_raw = _get_col_val('labor_cost')
        if lab_raw:
            lab_cost = _parse_row_value(lab_raw, 'labor_cost', 0)
            if lab_cost is None:
                errors.append({'row': row_num, 'reason': '노무비 형식 오류'})
                continue
        else:
            lab_cost = 0

        # 경비
        exp_raw = _get_col_val('expense_cost')
        if exp_raw:
            exp_cost = _parse_row_value(exp_raw, 'expense_cost', 0)
            if exp_cost is None:
                errors.append({'row': row_num, 'reason': '경비 형식 오류'})
                continue
        else:
            exp_cost = 0

        # 비고 (선택)
        note = _get_col_val('note')

        success.append({
            'work_name': work_name,
            'spec': spec,
            'unit': unit,
            'unit_quantity': unit_qty,
            'material_cost': mat_cost,
            'labor_cost': lab_cost,
            'expense_cost': exp_cost,
            'note': note,
        })

    return {'success': success, 'errors': errors}
