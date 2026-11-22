"""
Community Renewable Energy Awareness and Management Portal
Database Initialization and Seed Script
Supports both MySQL and SQLite configurations.
"""

import py_loader
import sys
from datetime import datetime
from app import create_app
from models import db, User, Project, CommunityPost, PostComment, EnergyTip, EducationalArticle, FeedbackMessage, SavedCalculation

def seed_database():
    app = create_app()
    with app.app_context():
        print(f"[*] Connected Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Reset if requested
        if "--reset" in sys.argv:
            print("[!] Dropping all existing tables...")
            db.drop_all()
            print("[+] Tables dropped.")

        print("[*] Creating database tables if they do not exist...")
        db.create_all()
        print("[+] Tables verified/created successfully.")

        # Check if users already exist
        if User.query.first():
            print("[i] Database already contains seed data. Run with '--reset' to re-seed.")
            return

        print("[*] Seeding default users (password: 'green123' / 'admin123')...")
        user1 = User(
            name="Elena Vance",
            email="elena@greenportal.org",
            role="admin",
            bio="Environmental engineer and coordinator of the Community Solar Cooperative.",
            location="Portland, OR",
            energy_interest="Microgrids & Solar Photovoltaics"
        )
        user1.set_password("admin123")

        user2 = User(
            name="Marcus Chen",
            email="marcus@cleanenergy.org",
            role="member",
            bio="Homeowner with an 8.4 kW rooftop solar and battery storage setup since 2023.",
            location="Denver, CO",
            energy_interest="Rooftop Solar & Home Battery Storage"
        )
        user2.set_password("green123")

        user3 = User(
            name="Sophia Rodriguez",
            email="sophia@ecocommunity.net",
            role="member",
            bio="Permaculture advocate and clean energy enthusiast working on biomass digestors.",
            location="Austin, TX",
            energy_interest="Biomass & Organic Waste Energy"
        )
        user3.set_password("green123")

        db.session.add_all([user1, user2, user3])
        db.session.commit()
        print("[+] Demo users created.")

        print("[*] Seeding Renewable Energy Projects...")
        projects = [
            Project(
                title="Sunny Heights Community Solar Farm",
                slug="sunny-heights-community-solar-farm",
                category="Solar",
                description="A joint neighborhood solar garden installed on unused municipal land, allowing 180 apartment residents and homeowners without suitable roofs to subscribe and offset their electric bills.",
                location="Oakridge District, Portland, OR",
                capacity="450 kW",
                annual_generation=680.0,
                co2_saved_annual=480.0,
                participants_count=185,
                status="Active",
                budget=520000.0,
                installation_guide="1. Site feasibility assessment;\n2. Community subscriber onboarding;\n3. Tier-1 monocrystalline bifacial panel mounting;\n4. Grid interconnect with net metering;\n5. Cloud inverter telemetry and monitoring.",
                image_url="solar_farm.svg",
                created_by_id=user1.id
            ),
            Project(
                title="Prairie Breeze Cooperative Wind Project",
                slug="prairie-breeze-cooperative-wind-project",
                category="Wind",
                description="Community-owned dual 850 kW wind turbines powering agricultural processing, community centers, and local schools with 100% clean kinetic wind energy.",
                location="Meadow Valley County, CO",
                capacity="1.7 MW",
                annual_generation=4200.0,
                co2_saved_annual=2940.0,
                participants_count=310,
                status="Active",
                budget=2100000.0,
                installation_guide="1. Wind resource LiDAR measurement over 12 months;\n2. Environmental and avian impact clearance;\n3. Foundation concrete pouring and tower erection;\n4. Grid synchronization and supervisory SCADA control.",
                image_url="wind_project.svg",
                created_by_id=user1.id
            ),
            Project(
                title="Clear Creek Micro-Hydro Generation Station",
                slug="clear-creek-micro-hydro-generation-station",
                category="Hydro",
                description="Low-impact run-of-river micro-hydro electric installation providing steady, non-intermittent baseline power to 75 mountain valley households without damming the creek.",
                location="Cascade Foothills, WA",
                capacity="120 kW",
                annual_generation=850.0,
                co2_saved_annual=595.0,
                participants_count=75,
                status="Active",
                budget=280000.0,
                installation_guide="1. Intake screen installation with fish-friendly diversion;\n2. Penstock pipe laying along terrain slope;\n3. Pelton impulse turbine and induction generator setup;\n4. Automated flow control valve system.",
                image_url="hydro_project.svg",
                created_by_id=user1.id
            ),
            Project(
                title="GreenFields Agricultural Biomass & Biogas Unit",
                slug="greenfields-agricultural-biomass-biogas-unit",
                category="Biomass",
                description="Anaerobic digester facility converting farm organic matter, crop residues, and animal manure into clean biogas for electricity generation and nutrient-rich biofertilizer.",
                location="Central Valley Agro-District, CA",
                capacity="350 kW",
                annual_generation=2100.0,
                co2_saved_annual=1470.0,
                participants_count=92,
                status="Active",
                budget=750000.0,
                installation_guide="1. Anaerobic digester tank sealing and heating loops;\n2. Biogas collection dome and sulfur removal scrubber;\n3. Combined Heat and Power (CHP) engine integration;\n4. High-grade organic biofertilizer separator.",
                image_url="biomass_project.svg",
                created_by_id=user2.id
            ),
            Project(
                title="Sunset Ridge Community Rooftop Microgrid",
                slug="sunset-ridge-community-rooftop-microgrid",
                category="Solar",
                description="An interconnected network of 45 residential rooftops equipped with smart hybrid inverters and localized LFP battery storage for community resilience during blackouts.",
                location="Sunset Ridge, Austin, TX",
                capacity="225 kW",
                annual_generation=340.0,
                co2_saved_annual=238.0,
                participants_count=45,
                status="Planning",
                budget=390000.0,
                installation_guide="1. Structural roof inspections and electrical upgrades;\n2. Standardized 5kW solar + 10kWh battery kits;\n3. Smart gateway for peer-to-peer virtual power plant coordination.",
                image_url="microgrid_project.svg",
                created_by_id=user3.id
            )
        ]
        db.session.add_all(projects)
        db.session.commit()
        print("[+] Projects seeded.")

        print("[*] Seeding Energy Tips...")
        tips = [
            EnergyTip(
                title="Switch to High-Efficiency LED Lighting",
                category="Lighting",
                description="Replace remaining incandescent and halogen bulbs with ENERGY STAR certified LEDs. They use up to 75% less energy and last up to 25 times longer.",
                potential_savings_kwh=45,
                difficulty="Easy",
                icon="bi-lightbulb"
            ),
            EnergyTip(
                title="Install a Smart Programmable Thermostat",
                category="Heating & Cooling",
                description="Automate temperature setbacks when sleeping or away from home. Adjusting 7-10°F for 8 hours daily can save up to 10% on annual HVAC costs.",
                potential_savings_kwh=120,
                difficulty="Moderate",
                icon="bi-thermometer-half"
            ),
            EnergyTip(
                title="Eliminate Phantom Standby Energy Drain",
                category="Appliances",
                description="Use smart power strips that cut power to TVs, soundbars, gaming consoles, and computer peripherals when idle, eliminating 5-10% in vampire draw.",
                potential_savings_kwh=35,
                difficulty="Easy",
                icon="bi-plug"
            ),
            EnergyTip(
                title="Optimize Refrigerator and Freezer Temperatures",
                category="Kitchen & Appliances",
                description="Keep refrigerator temperature between 35°F and 38°F (1.7°C to 3.3°C) and freezer at 0°F (-18°C). Keep condenser coils dust-free.",
                potential_savings_kwh=25,
                difficulty="Easy",
                icon="bi-snow"
            ),
            EnergyTip(
                title="Wash Laundry in Cold Water",
                category="Appliances",
                description="About 75% to 90% of electricity used by washing machines goes toward heating the water. Cold water detergents clean effectively with zero heat penalty.",
                potential_savings_kwh=40,
                difficulty="Easy",
                icon="bi-droplet-half"
            ),
            EnergyTip(
                title="Seal Air Leaks Around Windows and Doors",
                category="Home",
                description="Apply weatherstripping and silicone caulk around drafty window frames, exterior doors, and attic hatches to keep conditioned air inside.",
                potential_savings_kwh=95,
                difficulty="Moderate",
                icon="bi-house-heart"
            ),
            EnergyTip(
                title="Regular Solar Panel Inspection & Dust Cleaning",
                category="Solar Tips",
                description="Wipe down solar panels twice a year in dusty regions to prevent soiling losses, which can otherwise decrease generation output by 5-15%.",
                potential_savings_kwh=80,
                difficulty="Easy",
                icon="bi-sun"
            )
        ]
        db.session.add_all(tips)
        db.session.commit()
        print("[+] Energy tips seeded.")

        print("[*] Seeding Educational Articles...")
        articles = [
            EducationalArticle(
                title="The Complete Guide to Solar Photovoltaic Systems",
                slug="complete-guide-to-solar-pv",
                category="Solar",
                summary="Discover how semiconductor solar cells convert irradiance directly into clean electricity for homes and businesses.",
                content="Solar photovoltaic (PV) technology harnesses solar irradiance through semiconductor silicon cells. When sunlight strikes the cell, photons energize electrons, generating a Direct Current (DC). An inverter then converts this DC into standard Alternating Current (AC) for household appliances.\n\nKey Advantages:\n- Zero operational greenhouse gas emissions and air pollutants.\n- Abundant, inexhaustible resource across all inhabited continents.\n- Minimal moving parts resulting in 25 to 30-year operational lifespans.\n- Modular scalability from 1 kW residential setups to 500 MW utility arrays.\n\nChallenges & Solutions:\n- Intermittency: Solved through advanced lithium iron phosphate (LFP) energy storage and smart grid interconnections.\n- Upfront capital expense: Substantially reduced by government incentives, solar tax credits, and community group buys.",
                read_time="6 min read",
                icon="bi-sun-fill"
            ),
            EducationalArticle(
                title="Harnessing the Wind: From Gentle Breezes to Community Turbines",
                slug="harnessing-the-wind-turbines",
                category="Wind",
                summary="Learn how aerodynamic turbine blades convert kinetic wind energy into clean mechanical and electrical power.",
                content="Wind power utilizes aerodynamic lift principles similar to aircraft wings. Moving air passes over curved turbine blades, creating lift and driving a central rotor connected through a gearbox to a high-efficiency generator.\n\nAdvantages:\n- Exceptional energy return on investment (EROI).\n- Compact land footprint; farming and cattle grazing continue right beneath the towers.\n- Very low lifecycle carbon footprint (under 11 grams of CO2 equivalent per kWh generated).\n\nConsiderations:\n- Site-dependent wind resource requirements requiring average speeds above 4.5 m/s.\n- Siting assessments required to protect local bird and bat migration corridors.",
                read_time="5 min read",
                icon="bi-wind"
            ),
            EducationalArticle(
                title="Micro-Hydro and Run-of-River Power for Mountain Communities",
                slug="micro-hydro-run-of-river",
                category="Hydro",
                summary="How flowing streams deliver steady, baseline renewable electricity without ecological disturbance or large reservoirs.",
                content="Micro-hydro systems harness the kinetic and gravitational potential energy of falling water. Unlike mega-dams that flood valleys, run-of-river installations divert a fraction of a stream through a sloped penstock to spin a Pelton or Turgo turbine, returning the water immediately downstream unharmed.\n\nAdvantages:\n- High reliability factor (often 70% to 90% capacity factor, running 24/7 day and night).\n- Extremely high energy density compared to solar or wind on equivalent footprint.\n- Decades-long service life with basic preventive maintenance.",
                read_time="4 min read",
                icon="bi-water"
            ),
            EducationalArticle(
                title="Biomass and Biogas: Transforming Organic Waste into Circular Energy",
                slug="biomass-and-biogas-circular-energy",
                category="Biomass",
                summary="Explore the role of agricultural residues, food waste, and organic matter in closing the carbon loop and providing renewable baseload energy.",
                content="Biomass energy captures energy stored in chemical bonds of organic materials. Through anaerobic digestion or gasification, organic matter such as crop husks, livestock manure, and municipality food scrap is broken down by microorganisms into methane-rich biogas, which fuels clean combustion engines.\n\nAdvantages:\n- Diverts methane-emitting organic waste from municipal landfills.\n- Produces high-value organic biofertilizer as a by-product.\n- Provides controllable, on-demand dispatchable renewable power.",
                read_time="5 min read",
                icon="bi-tree-fill"
            ),
            EducationalArticle(
                title="How Clean Energy Drastically Reduces Pollution & Protects Public Health",
                slug="how-clean-energy-reduces-pollution",
                category="Environment",
                summary="Understanding the immediate health and environmental dividends of transitioning away from fossil fuel combustion.",
                content="Fossil fuel power plants are major emitters of sulfur dioxide (SO2), nitrogen oxides (NOx), mercury, and fine particulate matter (PM2.5). These airborne pollutants contribute heavily to urban smog, respiratory illnesses, cardiovascular disease, and acid rain.\n\nRenewable energy sources produce zero direct combustion emissions during electric generation:\n1. PM2.5 Reduction: Prevents microscopic particles from entering human lungs and bloodstream.\n2. Ozone & Smog Mitigation: Eliminates NOx precursors that react with sunlight on hot summer days.\n3. Water Conservation: Solar PV and wind require virtually zero water for cooling, preserving billions of gallons of freshwater annually.\n4. Climate Stabilization: Eliminates CO2 and nitrous oxides driving climate extremes.",
                read_time="5 min read",
                icon="bi-shield-check"
            )
        ]
        db.session.add_all(articles)
        db.session.commit()
        print("[+] Educational articles seeded.")

        print("[*] Seeding Community Posts and Comments...")
        post1 = CommunityPost(
            user_id=user2.id,
            title="My First Year with an 8.4 kW Rooftop Solar System: Real Numbers and Tips",
            category="Solar Experience",
            content="We installed 21 monocrystalline panels with microinverters last spring. Over 12 months, our electricity bill dropped from an average of $215/month to just the $14 grid connection fee! We produced 11,200 kWh and even accumulated $180 in net metering credits during summer. For anyone considering it: make sure to trim overhanging branches and opt for microinverters if you have partial morning shade.",
            upvotes=24
        )
        post2 = CommunityPost(
            user_id=user3.id,
            title="How our neighborhood organized a collective bulk-purchasing program",
            category="Policy & Subsidy",
            content="By bundling 28 households together, we negotiated a 22% discount with a certified local solar installer! We also leveraged the 30% clean energy tax credit and local municipal rebates. The whole process took 4 months from informational meetings to first panel energization. Happy to share our RFP template with anyone interested!",
            upvotes=19
        )
        post3 = CommunityPost(
            user_id=user1.id,
            title="Understanding Net Metering vs Time-of-Use (TOU) Rates in 2026",
            category="Energy Tips",
            content="Utility rate structures are evolving rapidly. With Time-of-Use rates, electricity is most expensive between 4 PM and 9 PM. If you pair your solar panels with a modest 5-10 kWh battery, you can discharge battery power during peak hours and sell excess solar during high-rate intervals, drastically increasing your annual financial savings.",
            upvotes=15
        )
        db.session.add_all([post1, post2, post3])
        db.session.commit()

        c1 = PostComment(
            post_id=post1.id,
            user_id=user3.id,
            content="Incredible results Marcus! How did the snow in winter affect your generation in Colorado?"
        )
        c2 = PostComment(
            post_id=post1.id,
            user_id=user2.id,
            content="Thanks Sophia! The panels are installed at a 35-degree tilt, so snow usually slides off within 24-48 hours once the sun peeks out. Losses were less than 5% over winter!"
        )
        c3 = PostComment(
            post_id=post2.id,
            user_id=user1.id,
            content="Collective purchasing is the gold standard for accelerating community renewable adoption. Great work!"
        )
        db.session.add_all([c1, c2, c3])

        # Seed sample feedback
        fb = FeedbackMessage(
            name="David Miller",
            email="david.m@example.com",
            subject="Inquiry regarding Community Solar Subscription",
            category="Inquiry",
            message="Hello! Our family lives in an apartment building in the Oakridge district. How can we enroll in the Sunny Heights Community Solar Farm to receive clean power credits on our monthly utility bill?",
            status="New"
        )
        db.session.add(fb)

        # Seed sample saved calculation
        calc = SavedCalculation(
            user_id=user2.id,
            monthly_bill=210.0,
            monthly_kwh=1050.0,
            tariff_rate=0.20,
            roof_area_sqft=650.0,
            sunlight_hours=5.2,
            recommended_kw=7.5,
            monthly_savings=185.0,
            annual_savings=2220.0,
            co2_reduction_tons=8.2,
            trees_equivalent=135,
            payback_years=5.8
        )
        db.session.add(calc)

        db.session.commit()
        print("[+] Community posts, comments, sample calculation, and feedback seeded successfully.")
        print("[*] Database initialization completed successfully!")

if __name__ == '__main__':
    seed_database()
