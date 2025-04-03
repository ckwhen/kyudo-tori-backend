from app.seeds.dans_seed import seed as seed_dans

def seed_all():
    seed_dans()
    print("All seed data has been inserted!")

if __name__ == '__main__':
    seed_all()
