# Confirmatory analysis.
#
#   Rscript analysis/confirmatory.R
#
# Follows the analysis plan registered at https://doi.org/10.17605/OSF.IO/3NZA7
#
# Alpha 0.05, two-tailed throughout, including for the directional hypotheses,
# as the more conservative choice. Holm correction across the three
# confirmatory inferential tests (H1, H2, H3). H4 is a descriptive comparison
# of effect sizes with no significance test, the samples being
# non-commensurable. H5 and H6 are exploratory, uncorrected, and labelled so.

suppressPackageStartupMessages({
  library(ordinal)
  library(lme4)
  library(lmerTest)
  library(emmeans)
})

DATA <- "data/processed/nbk_study1.csv"
OUT  <- "analysis/confirmatory_output.txt"

sink(OUT, split = TRUE)

cat("CONFIRMATORY ANALYSIS\n")
cat("Preregistration: https://doi.org/10.17605/OSF.IO/3NZA7\n")
cat("Run:", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n\n")

d <- read.csv(DATA, stringsAsFactors = FALSE)
cat("rows read:", nrow(d), "\n")

# --- exclusions, per the registered criterion --------------------------------
d <- subset(d, parse_status %in% c("ok", "ok_word"))
cat("rows after exclusion:", nrow(d), "\n")
cat("exclusion rate:", sprintf("%.4f", 1 - nrow(d) / 2400), "\n\n")

rat <- subset(d, measure == "rating")
fc  <- subset(d, measure == "forced_choice")
cat("rating responses:", nrow(rat), "  forced-choice responses:", nrow(fc), "\n\n")

# --- factor coding, per the registered scheme --------------------------------
# version: reference level is the version NBK classified as the morally bad
# change, so a positive coefficient is the predicted direction. NBK classified
# version a as good on every moral item, so b is the reference.
prep <- function(x) {
  x$version    <- relevel(factor(x$version), ref = "b")
  x$item_class <- relevel(factor(x$item_class), ref = "preference")
  x$frame      <- relevel(factor(x$frame), ref = "minimal")
  x$model_key  <- relevel(factor(x$model_key), ref = "haiku")
  x$item_id    <- factor(x$item_id)
  x$rating_num <- as.numeric(x$rating)
  x$rating_f   <- factor(x$rating_num, levels = 1:9, ordered = TRUE)
  x
}
rat <- prep(rat)
fc  <- prep(fc)

moral <- subset(rat, item_class == "moral")
moral$item_id <- droplevels(moral$item_id)

pvals <- c()

# =============================================================================
cat(strrep("=", 78), "\n")
cat("H1  Moral asymmetry: rating higher for the NBK-good version\n")
cat(strrep("=", 78), "\n\n")

h1 <- clmm(rating_f ~ version * model_key + frame + (1 | item_id),
           data = moral, link = "logit")
print(summary(h1))

co <- coef(summary(h1))
vrow <- grep("^versiona$", rownames(co))
cat("\nH1 test on the version term:\n")
cat("  estimate (log odds):", sprintf("%.3f", co[vrow, 1]), "\n")
cat("  odds ratio:         ", sprintf("%.2f", exp(co[vrow, 1])), "\n")
cat("  p:                  ", format.pval(co[vrow, 4], digits = 3), "\n")
pvals["H1"] <- co[vrow, 4]

cat("\nLinear mixed model, reported alongside as registered:\n")
h1lm <- lmer(rating_num ~ version * model_key + frame + (1 | item_id),
             data = moral)
print(summary(h1lm)$coefficients[1:2, , drop = FALSE])

# =============================================================================
cat("\n\n", strrep("=", 78), "\n")
cat("H2  Non-moral control: the asymmetry is smaller on preference items\n")
cat(strrep("=", 78), "\n\n")

h2 <- clmm(rating_f ~ version * item_class + model_key + frame + (1 | item_id),
           data = rat, link = "logit")
print(summary(h2))

co2 <- coef(summary(h2))
irow <- grep("versiona:item_classmoral", rownames(co2))
cat("\nH2 test on the version x item_class interaction:\n")
cat("  estimate (log odds):", sprintf("%.3f", co2[irow, 1]), "\n")
cat("  odds ratio:         ", sprintf("%.2f", exp(co2[irow, 1])), "\n")
cat("  p:                  ", format.pval(co2[irow, 4], digits = 3), "\n")
pvals["H2"] <- co2[irow, 4]

# =============================================================================
cat("\n\n", strrep("=", 78), "\n")
cat("H3  Convergent validity: rating against forced choice\n")
cat(strrep("=", 78), "\n\n")

cell <- function(x, fn, col) {
  aggregate(x[[col]], by = list(item_id = x$item_id, version = x$version,
                                frame = x$frame, model_key = x$model_key),
            FUN = fn)
}
mr <- cell(rat, mean, "rating_num")
names(mr)[5] <- "mean_rating"
fc$is_true <- as.integer(fc$choice == "a")
ts <- cell(fc, mean, "is_true")
names(ts)[5] <- "true_self_prop"

j <- merge(mr, ts, by = c("item_id", "version", "frame", "model_key"))
cat("cells joined:", nrow(j), "\n\n")

sp <- cor.test(j$mean_rating, j$true_self_prop, method = "spearman",
               exact = FALSE)
print(sp)
pvals["H3"] <- sp$p.value

cat("\nBy model, since the pooled correlation may conceal divergence:\n")
for (m in levels(j$model_key)) {
  s <- subset(j, model_key == m)
  r <- suppressWarnings(cor(s$mean_rating, s$true_self_prop,
                            method = "spearman"))
  cat(sprintf("  %-8s rho = %6.3f   (n = %d)\n", m, r, nrow(s)))
}

# =============================================================================
cat("\n\n", strrep("=", 78), "\n")
cat("Holm correction across the three confirmatory tests\n")
cat(strrep("=", 78), "\n\n")
adj <- p.adjust(pvals, method = "holm")
for (h in names(pvals)) {
  cat(sprintf("  %-4s raw p = %-12s holm p = %-12s\n", h,
              format.pval(pvals[h], digits = 3),
              format.pval(adj[h], digits = 3)))
}

# =============================================================================
cat("\n\n", strrep("=", 78), "\n")
cat("H4  Magnitude against the human benchmark (descriptive)\n")
cat(strrep("=", 78), "\n\n")

# Partial eta-squared for the version effect from the linear mixed model,
# via the F statistic from a type III anova.
av <- anova(h1lm)
fv <- av["version", "F value"]
df1 <- av["version", "NumDF"]
df2 <- av["version", "DenDF"]
peta <- (fv * df1) / (fv * df1 + df2)
cat("version effect, linear mixed model:\n")
cat(sprintf("  F(%.0f, %.1f) = %.1f\n", df1, df2, fv))
cat(sprintf("  partial eta-squared = %.3f\n\n", peta))

cat("Human benchmarks:\n")
cat("  Newman, Bloom & Knobe (2014) Study 1: 0.39 forced choice, 0.33 continuous\n")
cat("  Lee & Feldman (2025), N = 803:        0.20 forced choice, 0.22 continuous\n\n")
cat("No significance test is applied. The samples are not commensurable.\n")

cat("\nRaw difference in mean rating by model, moral items:\n")
for (m in levels(moral$model_key)) {
  s <- subset(moral, model_key == m)
  a <- mean(s$rating_num[s$version == "a"])
  b <- mean(s$rating_num[s$version == "b"])
  cat(sprintf("  %-8s a = %.2f   b = %.2f   difference = %+.2f\n", m, a, b, a - b))
}

# =============================================================================
cat("\n\n", strrep("=", 78), "\n")
cat("H5  Prompt frame (exploratory, uncorrected)\n")
cat(strrep("=", 78), "\n\n")

h5 <- clmm(rating_f ~ version * frame + model_key + (1 | item_id),
           data = moral, link = "logit")
print(summary(h5))

cat("\nMean rating by frame and version, moral items:\n")
print(round(tapply(moral$rating_num,
                   list(moral$frame, moral$version), mean), 2))

# =============================================================================
cat("\n\n", strrep("=", 78), "\n")
cat("H6  Between-model variation (exploratory, uncorrected)\n")
cat(strrep("=", 78), "\n\n")

cat("Pairwise contrasts of the version effect between models, Tukey adjusted:\n\n")
em <- emmeans(h1lm, ~ version | model_key)
print(pairs(em))
cat("\nDifferences between those contrasts:\n\n")
print(pairs(emmeans(h1lm, ~ version * model_key), by = NULL, adjust = "tukey")[1:10])

# =============================================================================
cat("\n\n", strrep("=", 78), "\n")
cat("Robustness\n")
cat(strrep("=", 78), "\n\n")

cat("Item nbk_s1_minorities was observed more heavily during piloting than any\n")
cat("other item and is reported separately, as registered.\n\n")
mm <- subset(moral, item_id == "nbk_s1_minorities")
for (m in levels(mm$model_key)) {
  s <- subset(mm, model_key == m)
  if (nrow(s) == 0) next
  a <- mean(s$rating_num[s$version == "a"])
  b <- mean(s$rating_num[s$version == "b"])
  cat(sprintf("  %-8s a = %.2f   b = %.2f   difference = %+.2f\n", m, a, b, a - b))
}

cat("\n\nLeave-one-item-out: version effect from the linear mixed model with\n")
cat("each moral item removed in turn.\n\n")
for (it in levels(moral$item_id)) {
  s <- subset(moral, item_id != it)
  s$item_id <- droplevels(s$item_id)
  fit <- lmer(rating_num ~ version * model_key + frame + (1 | item_id), data = s)
  est <- fixef(fit)["versiona"]
  cat(sprintf("  without %-22s version estimate = %+.3f\n", it, est))
}

cat("\n\nProportional odds assumption, H1 model:\n")
cat("Comparing the fitted model against one allowing a category-specific\n")
cat("effect for version.\n\n")
po <- tryCatch({
  h1n <- clm(rating_f ~ version + model_key + frame, data = moral)
  h1s <- clm(rating_f ~ model_key + frame, nominal = ~ version, data = moral)
  print(anova(h1n, h1s))
  TRUE
}, error = function(e) {
  cat("  could not be evaluated:", conditionMessage(e), "\n")
  FALSE
})

cat("\n\nDone.\n")
sink()
cat("\nOutput written to", OUT, "\n")
