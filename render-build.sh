#!/usr/bin/env bash
# ติดตั้ง Library
pip install -r requirements.txt
# ติดตั้ง Browser และ Dependencies ที่จำเป็นในระบบ
playwright install chromium
playwright install-deps
