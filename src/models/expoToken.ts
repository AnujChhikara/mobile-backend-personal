import { Collection, ObjectId } from "mongodb";
import { getDatabase } from "../db/connection";

export interface ExpoToken {
  _id?: ObjectId;
  user_id: string;
  expo_token: string;
  created_at?: Date;
  updated_at?: Date;
}

export function getExpoTokensCollection(): Collection<ExpoToken> {
  const db = getDatabase();
  return db.collection<ExpoToken>("expo_tokens");
}
