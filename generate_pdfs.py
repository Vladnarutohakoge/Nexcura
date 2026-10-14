import os

def generate_pdf(path, title, subtitle, patient, doctor, date, sections):
    def escape_pdf(text):
        return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        
    content_lines = [
        'BT',
        '/F1 18 Tf',
        '50 740 Td',
        f'({escape_pdf(title)}) Tj',
        '/F1 12 Tf',
        '0 -24 Td',
        f'({escape_pdf(subtitle)}) Tj',
        '/F2 10 Tf',
        '0 -20 Td',
        f'({escape_pdf(f"Patient: {patient}    Date: {date}    Provider: {doctor}")}) Tj',
        '/F1 10 Tf',
        '0 -14 Td',
        '(---------------------------------------------------------------------------------------------------------------------------------) Tj',
    ]
    
    for header, rows in sections:
        content_lines.extend([
            '/F1 12 Tf',
            '0 -22 Td',
            f'({escape_pdf(header)}) Tj',
            '/F2 10 Tf',
            '0 -16 Td'
        ])
        for r in rows:
            content_lines.extend([
                f'({escape_pdf(r)}) Tj',
                '0 -14 Td'
            ])
            
    content_lines.append('ET')
    stream_data = '\n'.join(content_lines).encode('latin1')
    stream_len = len(stream_data)
    
    objects = [
        b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n',
        b'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n',
        b'3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> >>\nendobj\n',
        f'4 0 obj\n<< /Length {stream_len} >>\nstream\n'.encode('latin1') + stream_data + b'\nendstream\nendobj\n',
        b'5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n',
        b'6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n'
    ]
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(b'%PDF-1.4\n')
        offsets = [0]
        curr = len(b'%PDF-1.4\n')
        for obj in objects:
            offsets.append(curr)
            f.write(obj)
            curr += len(obj)
            
        xref_offset = curr
        f.write(f'xref\n0 {len(objects)+1}\n0000000000 65535 f \n'.encode('latin1'))
        for off in offsets[1:]:
            f.write(f'{off:010d} 00000 n \n'.encode('latin1'))
            
        f.write(f'trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n'.encode('latin1'))

docs = [
    ('static/documents/NexCura_BloodPanel_2026.pdf', 
     'NexCura Diagnostic Center - Blood Panel Report', 
     'Complete Metabolic & Hematology Analysis', 
     'Alex Morgan (ID: NXC-2026-00147)', 
     'Dr. Priya Sharma (General Practice)', 
     '14 Aug 2026', 
     [
         ('Complete Blood Count (CBC)', ['White Blood Cell (WBC): 6.8 x10^3 / uL (Reference: 4.0 - 11.0)', 'Red Blood Cell (RBC): 4.95 x10^6 / uL (Reference: 4.5 - 5.9)', 'Hemoglobin: 15.2 g/dL (Reference: 13.5 - 17.5)', 'Hematocrit: 44.8 % (Reference: 41.0 - 50.0)', 'Platelet Count: 245 x10^3 / uL (Reference: 150 - 450)']),
         ('Comprehensive Metabolic Panel', ['Fasting Glucose: 92 mg/dL (Reference: 70 - 99)', 'Blood Urea Nitrogen (BUN): 14 mg/dL (Reference: 7 - 20)', 'Creatinine: 0.95 mg/dL (Reference: 0.7 - 1.3)', 'eGFR: > 90 mL/min/1.73m2', 'Total Cholesterol: 182 mg/dL (Desirable: < 200)']),
         ('Physician Impression & Notes', ['All hematologic and metabolic markers are within expected clinical reference ranges.', 'No critical lab alerts. Continue current balanced diet and exercise regimen.', 'Next routine evaluation recommended in 12 months.'])
     ]),
    ('static/documents/NexCura_ChestXRay_Report_2026.pdf', 
     'NexCura Radiology Institute - Imaging Report', 
     'Chest X-Ray - Posterior-Anterior (PA) View', 
     'Alex Morgan (ID: NXC-2026-00147)', 
     'Dr. Ananya Iyer (Cardiology)', 
     '02 Aug 2026', 
     [
         ('Examination Details', ['Study: PA Chest Radiograph Digital', 'Indication: Routine pre-cardiology baseline assessment', 'Comparison: Baseline study 2024']),
         ('Radiological Findings', ['Lungs: Clear bilaterally. No active focal consolidation, pleural effusion, or pneumothorax.', 'Cardiothoracic Ratio: 0.44 (Normal < 0.50). Normal cardiac size and contour.', 'Mediastinum & Hila: Normal width and vascularity.', 'Osseous Structures & Soft Tissues: Intact ribs and clavicles. No acute abnormalities.']),
         ('Impression', ['Normal PA chest radiograph. No acute cardiopulmonary disease demonstrated.'])
     ]),
    ('static/documents/NexCura_HbA1c_Report_2026.pdf', 
     'NexCura Endocrinology Laboratory - Glycemic Profile', 
     'Glycated Hemoglobin (HbA1c) Monitoring Report', 
     'Alex Morgan (ID: NXC-2026-00147)', 
     'Dr. Rohan Mehta (Endocrinology)', 
     '20 Jul 2026', 
     [
         ('Glycemic Metrics', ['HbA1c: 5.6 % (Normal Reference: < 5.7 %, Prediabetes: 5.7 - 6.4 %)', 'Estimated Average Glucose (eAG): 114 mg/dL (Reference: 70 - 126)', 'Previous HbA1c (Jan 2026): 5.8 % (Change: -0.2 % improvement)']),
         ('Clinical Guidance', ['Patient demonstrates optimal glycemic control in the euglycemic range.', 'Current therapeutic regimen: Metformin 500mg daily is well-tolerated.', 'Schedule next follow-up glycated hemoglobin review in 6 months.'])
     ]),
    ('static/documents/NexCura_Discharge_Summary_2026.pdf', 
     'NexCura Central Hospital - Discharge Summary', 
     'Inpatient Clinical Summary & Home Care Plan', 
     'Alex Morgan (ID: NXC-2026-00147)', 
     'Dr. Arjun Mehta (Chief Medical Officer)', 
     '15 Jun 2026', 
     [
         ('Hospital Course', ['Admission Reason: Minor endoscopic surveillance procedure', 'Admission Date: 14 Jun 2026 | Discharge Date: 15 Jun 2026', 'Procedure: Diagnostic endoscopy with biopsy - Unremarkable findings']),
         ('Discharge Medications & Instructions', ['Resume regular medications with water and light meals.', 'Avoid strenuous heavy lifting for 48 hours.', 'Follow up with primary care physician Dr. Priya Sharma in 2 weeks.']),
         ('Emergency Contact', ['24/7 NexCura Rapid Helpline: +91 80 4912 9999 or call 112 immediately for acute symptoms.'])
     ]),
    ('static/documents/NexCura_Clinical_Policy_2026.pdf', 
     'NexCura Governance - Organization Access Policy', 
     'Role-Based Clinical Access and Data Governance Charter', 
     'NexCura Health System Administrator', 
     'Compliance & Data Protection Office', 
     '01 Sep 2026', 
     [
         ('Role Hierarchy & Privilege Separation', ['Administrator: Organization setup, user management, audit logs, facility operations.', 'Clinician / Physician: Assigned chart reviews, SOAP encounter documentation, trial enrollment.', 'Staff / Care Operations: Patient triage, admissions, bed scheduling, pharmacy order fulfillment.', 'Patient: Personal medical records, test results review, appointment scheduling, secure messaging.']),
         ('Audit & Data Protection Standard', ['All protected health information access is recorded in immutable cryptographic audit trails.', 'Zero unauthenticated database writes or clinical record modifications permitted.'])
     ]),
    ('static/documents/NexCura_Appointment_Report_2026.pdf', 
     'NexCura Operations - Appointment Volume Report', 
     'Weekly Departmental Throughput and Scheduling Metrics', 
     'NexCura System Operations', 
     'Healthcare Informatics Department', 
     '25 Sep 2026', 
     [
         ('Weekly Scheduling Performance', ['Monday: 42 In-Person / 14 Telehealth (Total: 56)', 'Tuesday: 38 In-Person / 12 Telehealth (Total: 50)', 'Wednesday: 45 In-Person / 18 Telehealth (Total: 63)', 'Thursday: 39 In-Person / 15 Telehealth (Total: 54)', 'Friday: 48 In-Person / 20 Telehealth (Total: 68)', 'Saturday: 28 In-Person / 8 Telehealth (Total: 36)']),
         ('Operational Summary', ['Overall Capacity Utilization: 88.4%', 'Average Patient Check-In Wait: 4.2 minutes', 'Provider Punctuality Score: 96.8%'])
     ])
]

if __name__ == '__main__':
    for p, t, s, pt, d, dt, sec in docs:
        generate_pdf(p, t, s, pt, d, dt, sec)
        print(f'Generated {p}: {os.path.getsize(p)} bytes')
    print('All PDFs generated successfully.')
