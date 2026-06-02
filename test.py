from services.database_service import get_company_info

print("Starting test...")

data = get_company_info("TCS")

print("Data received:")
print(data)

print("Test completed")