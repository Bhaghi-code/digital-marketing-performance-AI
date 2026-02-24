import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "data/marketing.db"
random.seed(7)

CHANNELS = ["Email", "Webinar", "Paid Search", "Organic Search", "LinkedIn", "Direct"]
CAMPAIGN_TYPES = ["Newsletter", "Product Launch", "Webinar Invite", "Case Study", "Free Trial", "Retargeting"]
REGIONS = ["NA", "EMEA", "APAC"]

def daterange(start_date, end_date):
    d = start_date
    while d <= end_date:
        yield d
        d += timedelta(days=1)

def create_tables(cur):
    cur.executescript("""
    DROP TABLE IF EXISTS daily_web_traffic;
    DROP TABLE IF EXISTS email_campaigns_daily;
    DROP TABLE IF EXISTS webinar_events;
    DROP TABLE IF EXISTS funnel_monthly;
    DROP TABLE IF EXISTS ab_tests;

    CREATE TABLE daily_web_traffic (
        date TEXT,
        channel TEXT,
        sessions INTEGER,
        users INTEGER,
        pageviews INTEGER,
        bounce_rate REAL,
        avg_session_duration_sec INTEGER,
        signups INTEGER
    );

    CREATE TABLE email_campaigns_daily (
        date TEXT,
        campaign_id TEXT,
        campaign_name TEXT,
        segment TEXT,
        region TEXT,
        sent INTEGER,
        delivered INTEGER,
        opened INTEGER,
        clicked INTEGER,
        unsubscribes INTEGER,
        conversions INTEGER
    );

    CREATE TABLE webinar_events (
        webinar_id TEXT,
        webinar_name TEXT,
        date TEXT,
        registrants INTEGER,
        attendees INTEGER,
        avg_watch_time_min REAL,
        demo_requests INTEGER,
        mqls INTEGER
    );

    CREATE TABLE funnel_monthly (
        month TEXT,
        visitors INTEGER,
        leads INTEGER,
        mql INTEGER,
        sql INTEGER,
        customers INTEGER,
        marketing_spend_usd REAL
    );

    CREATE TABLE ab_tests (
        experiment_id TEXT,
        experiment_name TEXT,
        start_date TEXT,
        end_date TEXT,
        variant TEXT,
        users INTEGER,
        conversions INTEGER
    );
    """)

def generate_daily_web_traffic(cur, start_date, end_date):
    for d in daterange(start_date, end_date):
        for ch in CHANNELS:
            base_sessions = {
                "Organic Search": 1800,
                "Paid Search": 1400,
                "Email": 900,
                "LinkedIn": 700,
                "Webinar": 450,
                "Direct": 1000,
            }[ch]

            seasonality = 1.0 + (0.12 if d.weekday() in [1,2,3] else -0.08)
            noise = random.uniform(0.75, 1.25)

            sessions = int(base_sessions * seasonality * noise)
            users = int(sessions * random.uniform(0.75, 0.95))
            pageviews = int(sessions * random.uniform(1.6, 2.8))
            bounce = round(random.uniform(0.35, 0.62) if ch in ["Paid Search", "LinkedIn"] else random.uniform(0.28, 0.55), 3)
            avg_dur = int(random.uniform(70, 210) if ch in ["Paid Search", "LinkedIn"] else random.uniform(90, 260))

            signup_rate = {
                "Email": 0.035,
                "Webinar": 0.045,
                "Paid Search": 0.018,
                "Organic Search": 0.022,
                "LinkedIn": 0.016,
                "Direct": 0.028,
            }[ch]
            signups = int(sessions * signup_rate * random.uniform(0.7, 1.3))

            cur.execute(
                "INSERT INTO daily_web_traffic VALUES (?,?,?,?,?,?,?,?)",
                (d.strftime("%Y-%m-%d"), ch, sessions, users, pageviews, bounce, avg_dur, signups)
            )

def generate_email_campaigns(cur, start_date, end_date):
    segments = ["Prospects", "Trial Users", "Customers", "Enterprise Leads"]
    for d in daterange(start_date, end_date):
        if random.random() < 0.55:
            continue

        n_campaigns = random.randint(1, 3)
        for _ in range(n_campaigns):
            campaign_id = f"EM-{d.strftime('%Y%m%d')}-{random.randint(100,999)}"
            cname = random.choice(CAMPAIGN_TYPES)
            segment = random.choice(segments)
            region = random.choice(REGIONS)

            sent = random.randint(8000, 45000)
            delivered = int(sent * random.uniform(0.985, 0.999))
            open_rate = random.uniform(0.22, 0.38) if segment in ["Prospects", "Enterprise Leads"] else random.uniform(0.28, 0.48)
            opened = int(delivered * open_rate)

            ctr = random.uniform(0.06, 0.14) if cname in ["Webinar Invite", "Case Study"] else random.uniform(0.04, 0.11)
            clicked = int(opened * ctr)

            unsub = int(delivered * random.uniform(0.0005, 0.0025))
            conv_rate = random.uniform(0.04, 0.11) if cname in ["Free Trial", "Retargeting"] else random.uniform(0.02, 0.07)
            conversions = int(clicked * conv_rate)

            cur.execute(
                "INSERT INTO email_campaigns_daily VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (d.strftime("%Y-%m-%d"), campaign_id, cname, segment, region,
                 sent, delivered, opened, clicked, unsub, conversions)
            )

def generate_webinars(cur, start_date, end_date):
    webinar_topics = ["AI for Marketing Ops", "B2B Personalization", "Attribution 101", "Conversion Optimization", "Analytics Best Practices"]
    current = start_date
    idx = 1
    while current <= end_date:
        current += timedelta(days=random.randint(7, 16))
        if current > end_date:
            break

        webinar_id = f"WB-{idx:03d}"
        wname = random.choice(webinar_topics)

        registrants = random.randint(400, 3200)
        attendance_rate = random.uniform(0.35, 0.62)
        attendees = int(registrants * attendance_rate)

        avg_watch = round(random.uniform(18, 46), 1)
        demo_requests = int(attendees * random.uniform(0.03, 0.12))
        mqls = int(attendees * random.uniform(0.07, 0.20))

        cur.execute(
            "INSERT INTO webinar_events VALUES (?,?,?,?,?,?,?,?)",
            (webinar_id, wname, current.strftime("%Y-%m-%d"), registrants, attendees, avg_watch, demo_requests, mqls)
        )
        idx += 1

def generate_funnel_monthly(cur, start_date, end_date):
    months = []
    d = datetime(start_date.year, start_date.month, 1)
    end_m = datetime(end_date.year, end_date.month, 1)
    while d <= end_m:
        months.append(d.strftime("%Y-%m"))
        d = datetime(d.year + (1 if d.month == 12 else 0), (1 if d.month == 12 else d.month + 1), 1)

    visitors = 120000
    for m in months:
        visitors = int(visitors * random.uniform(0.97, 1.06))
        leads = int(visitors * random.uniform(0.028, 0.042))
        mql = int(leads * random.uniform(0.35, 0.52))
        sql = int(mql * random.uniform(0.42, 0.62))
        customers = int(sql * random.uniform(0.18, 0.30))
        spend = round(random.uniform(120000, 260000), 2)

        cur.execute(
            "INSERT INTO funnel_monthly VALUES (?,?,?,?,?,?,?)",
            (m, visitors, leads, mql, sql, customers, spend)
        )

def generate_ab_tests(cur, start_date, end_date):
    experiments = [
        ("Landing Page CTA", "Increase trial starts"),
        ("Pricing Page Layout", "Increase demo requests"),
        ("Email Subject Line", "Increase opens"),
        ("Webinar Registration Flow", "Increase registrations"),
    ]

    for i, (name, goal) in enumerate(experiments, start=1):
        exp_id = f"AB-{i:03d}"
        s = start_date + timedelta(days=random.randint(10, 180))
        e = s + timedelta(days=random.randint(10, 28))
        if e > end_date:
            e = end_date

        base = 0.06 if "Landing" in name else (0.045 if "Pricing" in name else (0.28 if "Subject" in name else 0.12))
        uplift = random.uniform(0.01, 0.06)

        users_a = random.randint(6000, 22000)
        conv_a = int(users_a * base * random.uniform(0.9, 1.1))

        users_b = random.randint(6000, 22000)
        conv_b = int(users_b * (base * (1 + uplift)) * random.uniform(0.9, 1.1))

        cur.execute(
            "INSERT INTO ab_tests VALUES (?,?,?,?,?,?,?)",
            (exp_id, f"{name} — {goal}", s.strftime("%Y-%m-%d"), e.strftime("%Y-%m-%d"), "A", users_a, conv_a)
        )
        cur.execute(
            "INSERT INTO ab_tests VALUES (?,?,?,?,?,?,?)",
            (exp_id, f"{name} — {goal}", s.strftime("%Y-%m-%d"), e.strftime("%Y-%m-%d"), "B", users_b, conv_b)
        )

def main():
    start = datetime(2025, 1, 1)
    end = datetime(2025, 12, 31)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    create_tables(cur)
    generate_daily_web_traffic(cur, start, end)
    generate_email_campaigns(cur, start, end)
    generate_webinars(cur, start, end)
    generate_funnel_monthly(cur, start, end)
    generate_ab_tests(cur, start, end)

    conn.commit()
    conn.close()
    print(f"✅ Built SQLite DB at: {DB_PATH}")

if __name__ == "__main__":
    main()
