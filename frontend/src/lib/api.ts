import z from "zod";

const API_BASE_URL = "http://127.0.0.1:8000";

const responseSchema = z.object({
  filename: z.string(),
  imageId: z.string(),
});

export async function uploadImage(
  file: File
): Promise<{ filename: string; imageId: string }> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/api/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to upload image");
  }

  const validated = responseSchema.safeParse(await response.json());

  if (!validated.success) {
    throw new Error("Invalid response from server");
  }

  return validated.data;
}
