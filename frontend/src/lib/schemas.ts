import z from "zod";

export const FORMAT_VALUES = ["a3", "a4", "a5"] as const;

export const settingsFormSchema = z.object({
  filename: z.string().min(1, "Filename is required"),
  rgbColors: z
    .array(z.object({ value: z.string() }))
    .min(2, "At least two colors must be selected"),
  format: z.enum(FORMAT_VALUES),
  minWidth: z.number().min(0, "Minimum width must be a positive number"),
  targetPpi: z.number().min(1, "Target PPI must be a positive number"),
  bilateralFiltering: z.boolean(),
});

export type SettingsFormReturn = z.infer<typeof settingsFormSchema>;
