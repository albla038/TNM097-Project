import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Field,
  FieldContent,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSet,
} from "@/components/ui/field";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from "@/components/ui/input-group";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { zodResolver } from "@hookform/resolvers/zod";
import { RotateCw, X } from "lucide-react";
import { useEffect } from "react";
import { Controller, useFieldArray, useForm, useWatch } from "react-hook-form";
import { useDebounce } from "use-debounce";
import z from "zod";

const FORMAT_VALUES = ["a3", "a4", "a5"] as const;
const FORMAT_OPTIONS = [
  { value: FORMAT_VALUES[0], label: "A3 (297 x 420 mm)" },
  { value: FORMAT_VALUES[1], label: "A4 (210 x 297 mm)" },
  { value: FORMAT_VALUES[2], label: "A5 (148 x 210 mm)" },
] as const;

const randomHexColor = () =>
  "#" +
  Math.floor(Math.random() * 16777215)
    .toString(16)
    .padStart(6, "0");

const formSchema = z.object({
  filename: z.string().min(1, "Filename is required"),
  rgbColors: z
    .array(z.object({ value: z.string() }))
    .min(2, "At least two colors must be selected"),
  format: z.enum(FORMAT_VALUES),
  minWidth: z.number().min(0, "Minimum width must be a positive number"),
  targetPpi: z.number().min(1, "Target PPI must be a positive number"),
  bilateralFiltering: z.boolean(),
});

type FormValues = z.infer<typeof formSchema>;

type SettingsFormProps = {
  filename: string;
  onSetFilename: (filename: string) => void;
};

export default function SettingsForm({
  filename,
  onSetFilename,
}: SettingsFormProps) {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      filename: filename,
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

  const {
    fields: colorFields,
    append,
    remove,
  } = useFieldArray({
    control: form.control,
    name: "rgbColors",
  });

  // Watch and debounce all form values
  const watchedFormValues = useWatch({ control: form.control }) as FormValues;
  const [debouncedFormValues] = useDebounce(watchedFormValues, 300);

  // React to the debounced changes
  useEffect(() => {
    console.log(debouncedFormValues);
  }, [debouncedFormValues]);

  return (
    <FieldSet>
      <FieldLegend>Settings</FieldLegend>
      <FieldDescription>
        Adjust the settings below to customize your PDF template
      </FieldDescription>

      {/* Color selection */}
      <FieldSet>
        <FieldLegend variant="label">Colors</FieldLegend>
        <FieldDescription>
          Select the RGB colors to include in the template. You can add or
          remove colors as needed.
        </FieldDescription>

        <FieldGroup>
          <div className="grid grid-cols-3 gap-2">
            {colorFields.map((field, index) => (
              <Controller
                key={field.id}
                name={`rgbColors.${index}.value`}
                control={form.control}
                render={({ field: controllerField, fieldState }) => (
                  <Field
                    orientation="horizontal"
                    data-invalid={fieldState.invalid}
                  >
                    <FieldContent>
                      <InputGroup>
                        <InputGroupAddon align="inline-start">
                          {index + 1}
                        </InputGroupAddon>
                        <InputGroupInput
                          {...controllerField}
                          id={`rgb-colors-${index}`}
                          aria-invalid={fieldState.invalid}
                          placeholder="#ffffff"
                          type="color"
                        />
                        {colorFields.length > 2 && (
                          <InputGroupAddon align="inline-end">
                            <InputGroupButton
                              type="button"
                              variant="ghost"
                              size="icon-xs"
                              onClick={() => remove(index)}
                              aria-label={`Remove color ${index + 1}`}
                            >
                              <X />
                            </InputGroupButton>
                          </InputGroupAddon>
                        )}
                      </InputGroup>
                      {fieldState.invalid && (
                        <FieldError errors={[fieldState.error]} />
                      )}
                    </FieldContent>
                  </Field>
                )}
              />
            ))}
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={() => append({ value: randomHexColor() })}
          >
            Add Color
          </Button>
        </FieldGroup>
      </FieldSet>

      <FieldGroup>
        {/* Format selection */}
        <Controller
          name="format"
          control={form.control}
          render={({ field, fieldState }) => (
            <Field data-invalid={fieldState.invalid}>
              <FieldLabel htmlFor="format-select">Format</FieldLabel>
              <Select
                name={field.name}
                value={field.value}
                onValueChange={field.onChange}
              >
                <SelectTrigger
                  id="format-select"
                  aria-invalid={fieldState.invalid}
                >
                  <SelectValue placeholder="Select" />
                </SelectTrigger>
                <SelectContent>
                  {FORMAT_OPTIONS.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
            </Field>
          )}
        />

        {/* Minimum mm width selection */}
        <Controller
          name="minWidth"
          control={form.control}
          render={({ field, fieldState }) => (
            <Field>
              <FieldLabel>Minimum width</FieldLabel>
              <FieldDescription>
                Set the minimum width ({field.value} mm) for the paint regions.
                {/* Smaller widths will be merged with neighboring regions
                        to ensure they are large enough to be painted. */}
              </FieldDescription>
              <Slider
                value={[field.value]}
                onValueChange={(value) => field.onChange(value[0])}
                min={0.5}
                max={5}
                step={0.1}
              />
              {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
            </Field>
          )}
        />

        {/* Target PPI selection */}
        <Controller
          name="targetPpi"
          control={form.control}
          render={({ field, fieldState }) => (
            <Field>
              <FieldLabel>Target PPI</FieldLabel>
              <FieldDescription>
                Set the target ({field.value}) pixels per inch. Lower PPI will
                result in faster processing but less detail in the final
                template.
              </FieldDescription>
              <Slider
                value={[field.value]}
                onValueChange={(value) => field.onChange(value[0])}
                min={50}
                max={1200}
                step={50}
              />
              {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
            </Field>
          )}
        />

        {/* Bilateral filtering toggle */}
        <Controller
          name="bilateralFiltering"
          control={form.control}
          render={({ field, fieldState }) => (
            <Field orientation="horizontal">
              <Checkbox
                id="bilateral-filtering-checkbox"
                name={field.name}
                checked={field.value}
                onCheckedChange={field.onChange}
              />
              <FieldContent>
                <FieldLabel htmlFor="bilateral-filtering-checkbox">
                  Bilateral filtering
                </FieldLabel>
                {/* TODO: Improve description */}
                <FieldDescription>
                  Enable bilateral filtering to reduce noise while preserving
                  edges. This can lead to cleaner regions. Disable for faster
                  processing.
                </FieldDescription>
              </FieldContent>
              {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
            </Field>
          )}
        />
        {/* <Field>
          <Button type="submit">Generate PDF</Button>
        </Field> */}
      </FieldGroup>

      <Field orientation="horizontal" className="flex-row-reverse">
        <Button variant="outline" onClick={() => form.reset()}>
          <RotateCw /> Reset
        </Button>
      </Field>
    </FieldSet>
  );
}
