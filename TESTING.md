# Testing Guide - NAV-MIS v2.0.0

## Pre-Testing Checklist

- [x] Python 3.9+ installed
- [x] All dependencies installed (streamlit, pandas, python-dotenv)
- [x] Database initialized with default data
- [x] All modules importable
- [x] Authentication working

---

## 🧪 Testing Scenarios

### Scenario 1: Login & Dashboard Access

**Steps:**
1. Run `streamlit run app.py`
2. Wait for app to load at `http://localhost:8501`
3. Login with `ahmad.fauzi` / `admin123`
4. Observe dashboard loads with 3 metric cards
5. Verify 7 department tabs visible

**Expected Results:**
- ✅ Login successful
- ✅ Dashboard displays with all metrics
- ✅ No errors in console
- ✅ UI responsive and styled correctly

**Pass/Fail:** ___________

---

### Scenario 2: Department - Perencanaan (Design & Planning)

**Steps:**
1. Click "Desain & Perencanaan" tab
2. Observe current Master Schedule & PWBS
3. Modify Master Schedule to "Test Schedule Updated"
4. Click "Update Data Perencanaan" button
5. Verify success message appears

**Expected Results:**
- ✅ Form displays with current values
- ✅ Data updates successfully
- ✅ Green success toast appears
- ✅ Dashboard reloads with new data

**Pass/Fail:** ___________

---

### Scenario 3: Department - Produksi (Production)

**Steps:**
1. Click "Produksi Lapangan" tab
2. Adjust progress slider to 75%
3. Enter cost: 5,000,000 Rp
4. Click "Kirim Laporan Validasi Produksi"
5. Verify success message & metric updates

**Expected Results:**
- ✅ Slider works (0-100%)
- ✅ Number input accepts currency
- ✅ Update successful
- ✅ Total cost increases in metrics

**Pass/Fail:** ___________

---

### Scenario 4: Department - Pembelian (Procurement)

**Steps:**
1. Click "Pembelian & Logistik" tab
2. Enter vendor: "PT Test Steel"
3. Enter volume: 50 Ton
4. Select target date
5. Click "Ajukan Nota Permintaan Pembelian"
6. Verify warning toast with order details

**Expected Results:**
- ✅ Form submission works
- ✅ Form clears after submit
- ✅ Toast message displays order summary
- ✅ Data saved to database

**Pass/Fail:** ___________

---

### Scenario 5: Department - QA/QC

**Steps:**
1. Click "QA / QC" tab
2. Select different status from dropdown
3. Add inspection notes (optional)
4. Click "Validasi Dokumen Mutu"
5. Verify update successful

**Expected Results:**
- ✅ Dropdown has multiple status options
- ✅ Text area for notes works
- ✅ Update successful
- ✅ Status persists after reload

**Pass/Fail:** ___________

---

### Scenario 6: Department - Gudang (Warehouse)

**Steps:**
1. Click "Gudang Material" tab
2. Note current stock
3. Select "Material Masuk (Lolos Inspeksi)"
4. Enter quantity: 20 Ton
5. Click "Eksekusi Mutasi Gudang"
6. Verify stock increases
7. Repeat with "Pengambilan" - verify stock decreases

**Expected Results:**
- ✅ Stock display shows current amount
- ✅ Material input adds to stock
- ✅ Material output subtracts from stock
- ✅ Cannot withdraw more than available
- ✅ Success toast shows new stock

**Pass/Fail:** ___________

---

### Scenario 7: Department - Fasilitas (Facilities)

**Steps:**
1. Click "Manajemen Fasilitas" tab
2. Current facility status displayed
3. Select new status from dropdown
4. Add maintenance notes
5. Click "Update Log Fasilitas"
6. Verify update successful

**Expected Results:**
- ✅ Current status displayed
- ✅ Multiple status options available
- ✅ Update successful
- ✅ Changes persisted

**Pass/Fail:** ___________

---

### Scenario 8: Department - Eksekutif (Executive)

**Steps:**
1. Click "Eksekutif Pemantau" tab
2. Observe data table with all parameters
3. Scroll through table
4. Check budget utilization metric
5. Check inventory metric

**Expected Results:**
- ✅ Table displays all project data
- ✅ Table is scrollable
- ✅ Metrics accurate
- ✅ All calculations correct

**Pass/Fail:** ___________

---

### Scenario 9: Manajemen Data - View Users

**Steps:**
1. Click "Manajemen Data" in sidebar
2. Click "Manajemen Pengguna" tab
3. Observe users table

**Expected Results:**
- ✅ 8 default users displayed
- ✅ Columns: username, role, department, is_active
- ✅ Table formatted correctly

**Pass/Fail:** ___________

---

### Scenario 10: Manajemen Data - Edit Parameters

**Steps:**
1. In "Manajemen Data", click "Manajemen Data" tab
2. Click "Edit Parameter Data" expander
3. Select a parameter from dropdown
4. Modify value
5. Click "Simpan Perubahan"
6. Verify success & check other tabs

**Expected Results:**
- ✅ Dropdown shows all parameters
- ✅ Current value pre-filled
- ✅ Can edit value
- ✅ Changes reflected everywhere

**Pass/Fail:** ___________

---

### Scenario 11: Laporan - Financial Analysis

**Steps:**
1. Click "Laporan & Analisis" in sidebar
2. Click "Analisis Keuangan" tab
3. Observe budget parameters

**Expected Results:**
- ✅ Budget data displayed
- ✅ Shows Anggaran & Biaya Terpakai
- ✅ Calculations accurate

**Pass/Fail:** ___________

---

### Scenario 12: Laporan - Inventory Analysis

**Steps:**
1. In "Laporan & Analisis", click "Analisis Inventori" tab
2. Observe warehouse data

**Expected Results:**
- ✅ Inventory data displayed
- ✅ Shows stok material
- ✅ Current values accurate

**Pass/Fail:** ___________

---

### Scenario 13: Laporan - Audit Log

**Steps:**
1. In "Laporan & Analisis", click "Audit Log" tab
2. Observe audit entries
3. Verify user, action, timestamp data

**Expected Results:**
- ✅ Audit log displayed
- ✅ Shows user who made change
- ✅ Shows action and timestamp
- ✅ Recent entries at top

**Pass/Fail:** ___________

---

### Scenario 14: Pengaturan Sistem

**Steps:**
1. Click "Pengaturan Sistem" in sidebar
2. Click "Konfigurasi Umum" tab - verify app info
3. Click "Keamanan" tab - verify security settings
4. Click "Tentang Sistem" tab - read info

**Expected Results:**
- ✅ All settings displayed
- ✅ Version shows v2.0.0
- ✅ Security values shown
- ✅ About section informative

**Pass/Fail:** ___________

---

### Scenario 15: Logout

**Steps:**
1. Click "Keluar (Sign Out)" button in sidebar
2. App redirects to login page
3. Try to access dashboard - blocked
4. Login again with different user

**Expected Results:**
- ✅ Session cleared
- ✅ Redirects to login page
- ✅ Cannot access dashboard after logout
- ✅ Login with different user works

**Pass/Fail:** ___________

---

### Scenario 16: Error Handling - Empty Login

**Steps:**
1. At login page
2. Leave username & password empty
3. Click "Login"
4. Observe error message

**Expected Results:**
- ✅ Error toast displays
- ✅ Message: "Username dan password tidak boleh kosong"
- ✅ Not redirected

**Pass/Fail:** ___________

---

### Scenario 17: Error Handling - Invalid Login

**Steps:**
1. Enter invalid username & password
2. Click "Login"
3. Observe error message

**Expected Results:**
- ✅ Error toast displays
- ✅ Message: "Username atau password salah"
- ✅ Stay on login page

**Pass/Fail:** ___________

---

### Scenario 18: UI/UX - Dark Theme

**Steps:**
1. Login to app
2. Inspect colors & styling
3. Check sidebar styling
4. Check card/button styling
5. Check text colors

**Expected Results:**
- ✅ Dark background (#0b0f19)
- ✅ Cards have border styling
- ✅ Buttons are blue (#2563eb)
- ✅ Text readable on dark bg
- ✅ Consistent theme throughout

**Pass/Fail:** ___________

---

### Scenario 19: Performance - Data Load Time

**Steps:**
1. Login to dashboard
2. Note load time
3. Switch between tabs
4. Switch between pages

**Expected Results:**
- ✅ Initial load < 5 seconds
- ✅ Tab switching instant
- ✅ Page switching < 2 seconds
- ✅ No lag or freezing

**Pass/Fail:** ___________

---

### Scenario 20: Multi-User Testing

**Steps:**
1. Login as ahmad.fauzi (admin)
2. Update data in multiple departments
3. Logout & login as budi.santoso
4. Verify can see updated data
5. Try to update different department
6. Verify changes reflected for other users

**Expected Results:**
- ✅ Data changes visible across sessions
- ✅ Permissions working correctly
- ✅ No data conflicts
- ✅ Database consistency maintained

**Pass/Fail:** ___________

---

## 📊 Summary Results

| Test # | Scenario | Result | Notes |
|--------|----------|--------|-------|
| 1 | Login & Dashboard | | |
| 2 | Perencanaan | | |
| 3 | Produksi | | |
| 4 | Pembelian | | |
| 5 | QA/QC | | |
| 6 | Gudang | | |
| 7 | Fasilitas | | |
| 8 | Eksekutif | | |
| 9 | User Management | | |
| 10 | Edit Parameters | | |
| 11 | Financial Report | | |
| 12 | Inventory Report | | |
| 13 | Audit Log | | |
| 14 | System Settings | | |
| 15 | Logout | | |
| 16 | Empty Login Error | | |
| 17 | Invalid Login Error | | |
| 18 | Dark Theme UI | | |
| 19 | Performance | | |
| 20 | Multi-User | | |

---

## ✅ Sign-Off

**Tested By:** ___________________
**Date:** ___________________
**Overall Result:** PASS / FAIL

**Comments:**
_________________________________________________________________
_________________________________________________________________

---

**NAV-MIS v2.0.0 Testing Complete!** ✅
