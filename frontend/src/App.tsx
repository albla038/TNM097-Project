import { ImageUploadDropZone } from "@/components/image-upload-dropzone";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useEffect } from "react";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import SettingsForm from "@/components/settings-form";
import { useForm, useWatch } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useDebounce } from "use-debounce";
import { randomHexColor } from "@/lib/utils";
import { settingsFormSchema, type SettingsFormReturn } from "@/lib/schemas";

export default function App() {
  const settingsForm = useForm<SettingsFormReturn>({
    resolver: zodResolver(settingsFormSchema),
    defaultValues: {
      filename: "",
      rgbColors: [
        { value: randomHexColor() },
        { value: randomHexColor() },
        { value: randomHexColor() },
        { value: randomHexColor() },
        { value: randomHexColor() },
        { value: randomHexColor() },
      ],
      format: "a4",
      minWidth: 1.5,
      targetPpi: 300,
      bilateralFiltering: true,
    },
  });

  // Watch and debounce all form values
  const watchedFormValues = useWatch({
    control: settingsForm.control,
  }) as SettingsFormReturn;
  const [debouncedFormValues] = useDebounce(watchedFormValues, 300);

  // React to the debounced changes
  useEffect(() => {
    console.log(debouncedFormValues);
  }, [debouncedFormValues]);

  return (
    <div className="flex h-svh flex-col gap-4 p-6">
      <aside className="max-w-md">
        <Card className="gap-0">
          <CardHeader className="border-b">
            <CardTitle>Open PBN</CardTitle>
            <CardDescription>
              A free and open "Paint by Numbers" tool to convert images into PDF
              templates. Upload your image, select your desired colors and
              format, and let Open PBN do the rest!
            </CardDescription>
          </CardHeader>
          <ScrollArea className="h-[75svh]">
            <CardContent className="pt-4">
              {/* Image upload */}
              <ImageUploadDropZone
                onSetFilename={(filename) =>
                  settingsForm.setValue("filename", filename)
                }
              />

              <Separator className="my-4" />

              <SettingsForm form={settingsForm} />
            </CardContent>
          </ScrollArea>
        </Card>
      </aside>
    </div>
  );
}
