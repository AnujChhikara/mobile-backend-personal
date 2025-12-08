import { MongoClient, Db } from "mongodb";

let client: MongoClient | null = null;
let db: Db | null = null;

export async function connectToDatabase(): Promise<Db> {
  if (db) {
    return db;
  }

  const dbMode = process.env.DB_MODE || "docker";
  const databaseName = process.env.DATABASE_NAME || "expo_tokens_db";

  let connectionUri: string;

  if (dbMode === "atlas") {
    connectionUri = process.env.MONGO_ATLAS_URI || "";
    if (!connectionUri) {
      throw new Error("MONGO_ATLAS_URI is required when DB_MODE=atlas");
    }
  } else {
    // Docker mode
    const host = process.env.MONGO_DOCKER_HOST || "localhost";
    const port = process.env.MONGO_DOCKER_PORT || "27017";
    const user = process.env.MONGO_DOCKER_USER || "admin";
    const password = process.env.MONGO_DOCKER_PASSWORD || "password123";

    connectionUri = `mongodb://${user}:${password}@${host}:${port}/?authSource=admin`;
  }

  try {
    client = new MongoClient(connectionUri);
    await client.connect();
    db = client.db(databaseName);
    console.log(
      `Connected to MongoDB (${dbMode} mode) - Database: ${databaseName}`
    );
    return db;
  } catch (error) {
    console.error("Failed to connect to MongoDB:", error);
    throw error;
  }
}

export async function closeDatabaseConnection(): Promise<void> {
  if (client) {
    await client.close();
    client = null;
    db = null;
    console.log("MongoDB connection closed");
  }
}

export function getDatabase(): Db {
  if (!db) {
    throw new Error("Database not connected. Call connectToDatabase() first.");
  }
  return db;
}
