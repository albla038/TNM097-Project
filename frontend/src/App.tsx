import { ImageUploadDropZone } from "@/components/image-upload-dropzone";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useState } from "react";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import SettingsForm from "@/components/settings-form";

export function App() {
  const [filename, setFilename] = useState("ttest");

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
              <ImageUploadDropZone />
              <Separator className="my-4" />

              <SettingsForm filename={filename} onSetFilename={setFilename} />
            </CardContent>
          </ScrollArea>
        </Card>
      </aside>
    </div>
  );
}

export default App;
