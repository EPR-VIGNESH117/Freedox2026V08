from typing import Dict, Any, List
from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.faculty import FacultyMember
from app.models.qualification import FacultyQualification

def get_department_report(db: Session) -> Dict[str, Any]:
    all_faculty = db.query(FacultyMember).all()
    total_faculty = len(all_faculty)

    dept_groups = defaultdict(list)
    for f in all_faculty:
        dept_groups[f.department].append(f)

    departments_list = []
    for dept_name, faculty_list in dept_groups.items():
        count = len(faculty_list)
        total_exp = sum(f.years_of_experience for f in faculty_list)
        avg_exp = round(total_exp / count, 2) if count > 0 else 0.0

        desig_counts = defaultdict(int)
        degree_counts = defaultdict(int)
        for f in faculty_list:
            desig_counts[f.designation] += 1
            for q in f.qualifications:
                degree_counts[q.degree] += 1

        departments_list.append({
            "department": dept_name,
            "faculty_count": count,
            "avg_years_of_experience": avg_exp,
            "designation_breakdown": dict(desig_counts),
            "highest_degree_breakdown": dict(degree_counts)
        })

    return {
        "total_departments": len(departments_list),
        "total_faculty": total_faculty,
        "departments": departments_list
    }

def get_qualification_report(db: Session) -> Dict[str, Any]:
    all_faculty = db.query(FacultyMember).all()
    total_faculty = len(all_faculty)

    all_quals = db.query(FacultyQualification).all()
    total_quals = len(all_quals)

    # Count how many distinct faculty members hold each degree type
    degree_holders = defaultdict(set)
    for q in all_quals:
        degree_holders[q.degree.strip()].add(q.faculty_id)

    breakdown = []
    for degree_name, faculty_ids in degree_holders.items():
        holders_count = len(faculty_ids)
        pct = round((holders_count / total_faculty * 100), 2) if total_faculty > 0 else 0.0
        breakdown.append({
            "degree": degree_name,
            "total_holders": holders_count,
            "percentage_of_faculty": pct
        })

    # Sort breakdown by holder count descending
    breakdown.sort(key=lambda x: x["total_holders"], reverse=True)

    return {
        "total_faculty": total_faculty,
        "total_qualifications_recorded": total_quals,
        "qualifications_breakdown": breakdown
    }

def get_designation_report(db: Session) -> Dict[str, Any]:
    all_faculty = db.query(FacultyMember).all()
    total_faculty = len(all_faculty)

    desig_groups = defaultdict(list)
    for f in all_faculty:
        desig_groups[f.designation].append(f)

    designations_list = []
    for desig_name, faculty_list in desig_groups.items():
        count = len(faculty_list)
        total_exp = sum(f.years_of_experience for f in faculty_list)
        avg_exp = round(total_exp / count, 2) if count > 0 else 0.0

        dept_dist = defaultdict(int)
        for f in faculty_list:
            dept_dist[f.department] += 1

        designations_list.append({
            "designation": desig_name,
            "faculty_count": count,
            "avg_years_of_experience": avg_exp,
            "department_distribution": dict(dept_dist)
        })

    return {
        "total_faculty": total_faculty,
        "designations": designations_list
    }

def get_experience_report(db: Session) -> Dict[str, Any]:
    all_faculty = db.query(FacultyMember).all()
    total_faculty = len(all_faculty)
    overall_avg_exp = round(sum(f.years_of_experience for f in all_faculty) / total_faculty, 2) if total_faculty > 0 else 0.0

    brackets_def = [
        {"bracket": "0-3 years (Junior)", "min": 0, "max": 3},
        {"bracket": "4-7 years (Mid-Level)", "min": 4, "max": 7},
        {"bracket": "8-15 years (Senior)", "min": 8, "max": 15},
        {"bracket": "16+ years (Veteran / Lead)", "min": 16, "max": 999}
    ]

    brackets_result = []
    for b in brackets_def:
        in_bracket = [
            f for f in all_faculty
            if b["min"] <= f.years_of_experience <= b["max"]
        ]
        count = len(in_bracket)
        avg_exp = round(sum(f.years_of_experience for f in in_bracket) / count, 2) if count > 0 else 0.0

        faculty_summary = [
            {
                "id": f.id,
                "name": f.full_name,
                "department": f.department,
                "designation": f.designation,
                "years_of_experience": f.years_of_experience
            }
            for f in in_bracket
        ]

        brackets_result.append({
            "bracket": b["bracket"],
            "min_years": b["min"],
            "max_years": b["max"] if b["max"] != 999 else 99,
            "faculty_count": count,
            "avg_years_of_experience": avg_exp,
            "faculty_list": faculty_summary
        })

    return {
        "total_faculty": total_faculty,
        "overall_avg_experience": overall_avg_exp,
        "brackets": brackets_result
    }
